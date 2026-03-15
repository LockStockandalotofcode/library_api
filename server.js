// import the express module
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json()); // allows api to read json data

app.get('/', (req, res) => {
    res.send("Library API, go to /books to look at available books.")
})

// DATA
let users = [
    {id: 1, name: "Amy", borrowedBooks: [] },
    {id: 2, name: "Bob", borrowedBooks: [] },
    {id: 3, name: "Carey", borrowedBooks: [] },
    {id: 4, name: "Dan", borrowedBooks: [] }
];

const titles = ["Don Quixote" ,"Alice's Adventures in Wonderland","The Adventures of Huckleberry Finn","The Adventures of Tom Sawyer","Treasure Island","Pride and Prejudice","Wuthering Heights","Jane Eyre","Moby Dick","The Scarlet Letter "
];

const authors = ["Miguel de Cervantes","Lewis Carroll","Mark Twain","Mark Twain","Robert Louis Stevenson","Jane Austen","Emily Brontë","Charlotte Brontë","Herman Melville","Nathaniel Hawthorne"
];

let books = titles.map((title, i) => ({
    id: i + 1,
    title: title,
    author: authors[i],
    isAvailable: true,
    dueDate: null
}));

// ROUTEs

// GET: all books
app.get('/books', (req, res) => res.json(books));

// GET: all users
app.get('/users', (req, res) => res.json(users));

// POST: borrow a book
app.post('/borrow', (req, res) => {
    const userId = Number(req.body.userId);
    const bookId = Number(req.body.bookId);

    const user = users.find(u => u.id === userId);
    const book = books.find(b => b.id === bookId);

    // in case of error
    if(!book || !book.isAvailable) return res.status(400).json({error: "Book is not available."});

    if (user.borrowedBooks.length >= 2) {
        return res.status(400).json({error: "max limit of books that can be borrowed reached"});
    }
    const today = new Date();
    const dueDate = new Date();
    dueDate.setDate(today.getDate() + 7);

    //update data
    book.isAvailable = false;
    book.dueDate = dueDate.toDateString();
    user.borrowedBooks.push({
        bookId: book.id,
        title: book.title,
        returnBy: book.dueDate
    });

    res.status(200).json({message: "Done", user});
});

//Starting the server
app.listen(port, () => {
    console.log(`Server is running at port ${port}`);
});