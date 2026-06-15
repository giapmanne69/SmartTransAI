from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Glossary
from ..schemas import GlossaryCreate, GlossaryUpdate, GlossaryOut
from .auth import get_current_user
from ..models import User

router = APIRouter(prefix="/glossary", tags=["glossary"])

@router.get("/", response_model=List[GlossaryOut])
def get_glossary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Glossary).filter(Glossary.user_id == current_user.id).all()

@router.post("/", response_model=GlossaryOut, status_code=status.HTTP_201_CREATED)
def create_glossary_item(
    item_data: GlossaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_item = Glossary(
        user_id=current_user.id,
        source_term=item_data.source_term,
        target_term=item_data.target_term,
        notes=item_data.notes
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/{item_id}", response_model=GlossaryOut)
def update_glossary_item(
    item_id: int,
    item_data: GlossaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(Glossary).filter(Glossary.id == item_id, Glossary.user_id == current_user.id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Glossary item not found"
        )
    
    if item_data.source_term is not None:
        item.source_term = item_data.source_term
    if item_data.target_term is not None:
        item.target_term = item_data.target_term
    if item_data.notes is not None:
        item.notes = item_data.notes
        
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_glossary_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(Glossary).filter(Glossary.id == item_id, Glossary.user_id == current_user.id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Glossary item not found"
        )
    db.delete(item)
    db.commit()
    return None

import json
import re
from fastapi import UploadFile, File

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_glossary_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = file.file.read().decode("utf-8", errors="ignore")
    filename = file.filename.lower()
    
    terms_to_create = []
    
    # 1. Parse JSON
    if filename.endswith(".json"):
        try:
            data = json.loads(contents)
            if isinstance(data, list):
                for item in data:
                    source = item.get("source_term") or item.get("source") or item.get("en")
                    target = item.get("target_term") or item.get("target") or item.get("vi")
                    notes = item.get("notes") or item.get("desc") or ""
                    if source and target:
                        terms_to_create.append((source.strip(), target.strip(), notes.strip()))
            elif isinstance(data, dict):
                for en_term, vi_term in data.items():
                    if isinstance(vi_term, str):
                        terms_to_create.append((en_term.strip(), vi_term.strip(), ""))
                    elif isinstance(vi_term, dict):
                        target = vi_term.get("target_term") or vi_term.get("target") or vi_term.get("vi") or ""
                        notes = vi_term.get("notes") or ""
                        if target:
                            terms_to_create.append((en_term.strip(), target.strip(), notes.strip()))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Định dạng JSON không hợp lệ: {str(e)}")
            
    # 2. Parse Markdown (.md) or Text (.txt)
    elif filename.endswith(".md") or filename.endswith(".txt"):
        lines = contents.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Phân tích bảng Markdown: | English | Vietnamese | Notes |
            if line.startswith("|") and line.endswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    source = parts[1]
                    target = parts[2]
                    notes = parts[3] if len(parts) > 4 else ""
                    if source and target and source != "English" and not source.startswith("-"):
                        # Loại bỏ hàng phân cách (chứa gạch ngang)
                        if not all(c == '-' or c == ' ' for c in source) and not all(c == '-' or c == ' ' for c in target):
                            terms_to_create.append((source, target, notes))
                continue
                
            # Phân tích danh sách bullet: - English: Vietnamese hoặc - English - Vietnamese
            match = re.match(r"^[-*+]\s+([^:|-]+)[:|-]\s+(.+)$", line)
            if match:
                source = match.group(1).strip()
                target_value = match.group(2).strip()
                notes = ""
                # Tìm ghi chú nếu có trong ngoặc đơn ở cuối câu
                notes_match = re.search(r"\(([^)]+)\)$", target_value)
                if notes_match:
                    notes = notes_match.group(1).strip()
                    target_value = re.sub(r"\([^)]+\)$", "", target_value).strip()
                
                if source and target_value:
                    terms_to_create.append((source, target_value, notes))

    else:
        raise HTTPException(status_code=400, detail="Định dạng tệp không hỗ trợ. Vui lòng tải file .json hoặc .md/.txt")

    if not terms_to_create:
        raise HTTPException(status_code=400, detail="Không tìm thấy thuật ngữ hợp lệ nào trong tệp tải lên.")

    imported_count = 0
    for source, target, notes in terms_to_create:
        # Tránh trùng lặp thuật ngữ
        existing = db.query(Glossary).filter(
            Glossary.user_id == current_user.id,
            Glossary.source_term == source
        ).first()
        if existing:
            existing.target_term = target
            existing.notes = notes or existing.notes
        else:
            new_item = Glossary(
                user_id=current_user.id,
                source_term=source,
                target_term=target,
                notes=notes
            )
            db.add(new_item)
        imported_count += 1
        
    db.commit()
    return {"message": "Success", "imported_count": imported_count}

