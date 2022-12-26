# notable
#### Video Demo:  <https://youtu.be/RpdHbEy4EIw>
#### Reason Behind The Idea:
With week 8's homepage, I decided to fill my website's content with stories and experiences from my life; creating some sort of blog. I really liked the idea of creating something useful and personal for myself. Thus, after thorough considerations, I decided to make a note-taking website.

Throughout the course of CS50, I wrote down notes as I watched the lecture videos. A major downside to writing notes is that, it is quite permanent. It's rather difficult and troublesome to reorganise the points I've already written down especially if I was using a pen. With digital note-taking, reorganising is as easy as copy and pasting. Hence, the note-taking website; notable was born.

#### Description:
Notable is a note-taking website. Notable allows for multiple notes, like the pages in a notebook or the files in a folder. Users can add, edit or delete their own notes. Along with each note is a checkbox list and a notepad, todo and scribbles respectively. Everything is conveniently located within one webpage however, if users find the list of notes they own, todo or scribbles annoying, they can easily hide them with a click of a button and expand the note-taking area. There is no need to manually save your notes because everything is automatically saved into the SQL database every 5 seconds. To assist in note-taking, users can easily make lists and box-out text with a button. After the user is done taking notes, if the user closed the website without logging out, the website will remember them via sessions and keep them logged in.

#### Considerations:
I wanted to make the website as accessible as possible. I wanted the users to be able to take notes without any hassle, like opening a notebook and being able to immediately write in it. Thus, I originally did not want to implement accounts. However, I realised that without accounts, users can't save their notes. While I could use sessions to store the notes, all the notes will be lost if the session was cleared or the user changed to a different device. Therefore, using accounts and sessions allows user's digital notes to be portable.

I added 2 functionalities that I often use when writing notes; boxing words together and making lists.

I added todo because I find it useful having a side notepad to jot down and organise my points before I finally include it in my notes. It also serves as an area that users can keep note of things that don't really fit in their notes.

I added todo to keep track of the things I have to search or look up later. Many times while I'm taking my notes and watching the lecture videos, I'll remember something that I have to do or have something I'm not so sure of that I plan to look up. Todo is the perfect area to help me keep track of those things.

## Notable

#### Register
First thing users have to do is register for an account.
Username and password are required. If either is missing, a flashing message will remind users of it.
If both username and password are present, a check for the username is done, flashing another message if the username is taken.
Otherwise, an account is registered and the password is hashed.
Notable will automatically create their first notebook redirecting them to the login page.


#### Login
Next users have to log in with their account.
Username and password are required again. A check is done to ensure the username exists. Additionally, the hashed password is checked, ensuring it belongs to the correct username.
If log in is unsuccessful, a flashing message will appear.
If log in is successful, the session will take note of the user's id and top filename (more on this later) before redirecting them to the page webpage.


#### Log out
Logs users out and clear the session.


#### Index
On the main webpage, you'll see your list of filenames, notes, todo and scribbles. These are based on the session's user_id and filename which were previously saved when logging in.


##### [Creating new files]
If the user decides to add a new notebook, a name (filename) is required. The filename cannot be empty, missing and must be unique to the user. If the filename meets all the requirements, a new filename is added into the database.


##### [Changing files]
The list of filenames are clickable. Clicking any filename would allow the user to change from the current filename to the selected one. When a filename is clicked, the corresponding notes_id is sent to the server. The server that finds the filename of the notes_id and updates the session's filename and ultimately updating the index page.


##### [Editing filename]
Users can edit their filenames by double clicking on any of the filename. Users are required to type out a new filename and send the formdata by pressing enter. The new filename and notes_id of the file will be sent to the server where the filename of the notes_id will be updated to the new filename. Afterwards, the session's filename will be updated to the new filename, changing the user's webpage to the newly edited file. If they change their minds about editing the filename, they can click the cross button.


##### [Deleting file]
When users double click a filename, other than editing, they are also allowed to delete the file. If they click on the delete button, the notes_id of the selected file will be send and subsequently deleted by the server.


##### [Autosaving]
The webpage automatically turns the innerHTML of notes, todo and scribbles into formdata and send it to the server every 5 seconds.


## JavaScript
JavaScript is used for many things such as sending formdata to the servers and checking for double clicks.


##### [Fileindicator]
The Fileindicator function is called everytime the webpage is loaded.
It searches for the list of filenames and compares it to the title (Current Selected Filename). If they are equal, the filename is changed from black to white color.


##### [Doubleclick]
A one-time EventListener is added to every filename. When clicked, it will prevent the default of changing files and add another one-time EventListener on the clicked filename. If clicked for the second time, a form is created. An input for the newfilename, the corresponding notes_id, the cross button and the delete button are appended into the form. The form is then inserted before the clicked filename and hides the clicked filename. This enables changing filenames, cancelling edit and deleting filename. However, if the second click does occur within half a second of the first click, the default changing files will continue.


##### [deleteedit]
deleteedit is the function to cancel editting a filename. The cross button searches and compares the filename that is being editted with the list of filenames, revealing the original filename before deleting it's parentNode which includes the input for new filename, corresponding notes_id, cross button and delete button. deleteedit runs when the cross button is clicked.


##### [deletefile]
deletefile is the function that is responsible for Deleting file; It sends the formdata to the server. Afterwards, to clean up the HTML, it reloads the page. deletefile runs when the delete button is clicked.


##### [todo]
An EventListener is added to todo to automatically insert a checkbox whenever the user presses enter. This adds a checkbox at the end of the list and moves the user's cursor to it.


##### [autosaving]
formdata is created every 5 seconds that allows Autosaving.


##### [boxbutton]

1. finds how many lines are in the highlighted text
2. finds the longest line in the highlighted text
3. adds spacing so that the right most line will be aligned
4. adds the remaining lines to make a box
5. replaces the selected text with the boxed text


##### [collapsible]
todo, scribbles and folders are collapsible. Clicking their respective button will add or remove the active class which hides the elements. Depending on the size of the notes and the button that was pressed, the notes' width will increase or decrease to fill the screen.