from datetime import date

from sqlalchemy.orm import joinedload

from typing import Dict, List

from ..api import constants
from ..api.utils.typesense_utils import upsert_documents
from .models import Candidate
from .session import SessionLocal


def build_candidate_search_text(
    candidate: Candidate
) -> str:
    
    name: str = f"{candidate.first_name or ''} {candidate.last_name or ''}".strip()
    parts: List[str] = [name]

    if candidate.status:
        parts.append(f"Status: {candidate.status}")
    if candidate.address_city:
        parts.append(f"Location: {candidate.address_city}")

    if candidate.education:
        parts.append("\nEducation:")
        for edu in sorted(
            candidate.education,
            key=lambda e: e.start_date or date.min,
            reverse=True,
        ):
            tokens = []
            if edu.degree:
                tokens.append(edu.degree)
            if edu.school:
                tokens.append(f"at {edu.school}")
            if edu.city:
                tokens.append(f"({edu.city})")
            if edu.start_date or edu.end_date:
                s = str(edu.start_date.year) if edu.start_date else "?"
                e_yr = str(edu.end_date.year) if edu.end_date else "present"
                tokens.append(f"[{s}-{e_yr}]")
            line = "  - " + " ".join(tokens)
            if edu.comments:
                line += f"\n    {edu.comments}"
            parts.append(line)

    if candidate.work_experience:
        parts.append("\nWork Experience:")
        for exp in sorted(
            candidate.work_experience,
            key=lambda e: e.start_date or date.min,
            reverse=True,
        ):
            tokens = []
            if exp.title:
                tokens.append(exp.title)
            if exp.company_name:
                tokens.append(f"at {exp.company_name}")
            if exp.start_date or exp.end_date:
                s = str(exp.start_date.year) if exp.start_date else "?"
                e_yr = str(exp.end_date.year) if exp.end_date else "present"
                tokens.append(f"[{s}-{e_yr}]")
            line = "  - " + " ".join(tokens)
            if exp.comments:
                line += f"\n    {exp.comments}"
            parts.append(line)

    return "\n".join(parts)


def index_all_candidates() -> int:
    with SessionLocal() as session:
        candidates = (
            session.query(Candidate)
            .options(
                joinedload(Candidate.education),
                joinedload(Candidate.work_experience),
            )
            .all()
        )

        count = 0
        for candidate in candidates:
            name = f"{candidate.first_name or ''} {candidate.last_name or ''}".strip()
            search_text: str = build_candidate_search_text(candidate=candidate)

            doc: Dict = {
                "id": candidate.external_id,
                "search_text": search_text,
                "name": name,
                "status": candidate.status or "",
            }

            upsert_documents(
                doc=doc,
                schema=constants.CONSULTANT_SCHEMA["name"],
                client=constants.TS_CLIENT,
            )
            count += 1

    return count
