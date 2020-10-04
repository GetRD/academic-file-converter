from enum import Enum


# Map BibTeX to Academic publication types.
class PublicationType(Enum):
    Uncategorized = 0
    ConferencePaper = 1
    JournalArticle = 2
    Preprint = 3
    Report = 4
    Book = 5
    BookSection = 6
    Thesis = 7  # (v4.2+ required)
    Patent = 8  # (v4.2+ required)


PUB_TYPES = {
    "article": PublicationType.JournalArticle,
    "book": PublicationType.Book,
    "conference": PublicationType.ConferencePaper,
    "inbook": PublicationType.BookSection,
    "incollection": PublicationType.BookSection,
    "inproceedings": PublicationType.ConferencePaper,
    "manual": PublicationType.Report,
    "mastersthesis": PublicationType.Thesis,
    "misc": PublicationType.Uncategorized,
    "patent": PublicationType.Patent,
    "phdthesis": PublicationType.Thesis,
    "proceedings": PublicationType.Uncategorized,
    "report": PublicationType.Report,
    "thesis": PublicationType.Thesis,
    "techreport": PublicationType.Report,
    "unpublished": PublicationType.Preprint,
}
