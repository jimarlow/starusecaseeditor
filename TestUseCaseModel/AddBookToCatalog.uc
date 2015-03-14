:Schema:
UseCase.sss

:Name:
AddBookToCatalog

:Parents:
None

:Actors:
Librarian
Test

:Brief description:
The Librarian adds a new book to the library catalog.

:Preconditions:
The Librarian is logged on to OLAS.

:Flow of events:
The Librarian selects "add book".
The system asks for the BookDetails.
The Librarian enters the BookDetails.
include( Test3 )
The system adds the the new Book to the catalog.

:Postconditions:
A new Book has been added to the catalog.

:Alternative flows:
1. CancelAddBook
2. BookAlreadyExists