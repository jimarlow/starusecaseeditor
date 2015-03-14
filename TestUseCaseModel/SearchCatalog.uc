:Schema:
UseCase.sss

:Name:
SearchCatalog

:Parents:
None

:Actors:
Librarian
Borrower

:Brief description:
The searcher searches the catalog for a book

:Preconditions:
The searcher is logged on to OLAS.

:Flow of events:
1. The  searcher selects "find book".
2. The system asks for the SearchCriteria.
3. The searcher enters the SearchCriteria.
4. The system displays a list of all books that meet the SearchCriteria.
5. If the searcher clicks on a book in the list
6. The system displays BookDetails for that book

:Postconditions:
None

:Alternative flows:
CancelSearchCatalog
BookNotFound