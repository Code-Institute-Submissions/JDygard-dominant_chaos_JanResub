# Testing documentation

## Frontend HTML/JS testing
Cosmetically the frontend has 9 pages. Base.html contains the nav bar and the footer, as is tradition.

1. "Home," i.e. index.html.
2. Leaderboard
3. Library
4. Play
5. Profile
6. About
7. Login
8. Register
9. Character
***

### Nav bar
The nav bar consists of, essentially, three parts.

#### The top nav bar

Top nav bar contains the brand logo, login, register and logout functions. It also hosts the "hamburger" icon when the page collapses into mobile view.

All elements that require a login to use correctly are hidden to users who are not logged in. Likewise, a logged-in users will not see the register or login buttons.

#### The bottom nav bar
The bottom nav bar sits below the top nav bar, and has 6 navigable elements when logged in. On smaller screens, it collapses into a hamburger icon in the top nav bar.

#### Collapsed mobile nav
On smaller screens, all of the functionality of the navbar collapses into a hamburger icon for a sleeker site.
***

### Footer
The footer is fixed at the bottom of the page and contains three parts.

#### Back to top button
A small floating button is generated in the footer to allow the user to easily click to return to the top of the current page.

#### Patreon link
The upper footer contains a link to Patreon

#### Copyright
The lower footer contains a message with the dev's copyright information
***



https://user-images.githubusercontent.com/78797168/131670307-8e21a552-c9fd-4453-84b9-4f54433a99a1.mp4


### "Home" page
index.html is broken up into three basic parts.

#### Hero image
The upper section is a large banner image with an offset centered call-to-action to join the site. The call-to-action has several media breakpoints to keep it in an attractive and readable state on all screens.

#### Join the chaos
The middle section is a three tiered area containing general reasons a user might enjoy the site. JavaScript is used to flip the middle section upon collapsing into a single column for a uniform look.

#### Join the fight Today!
The final section is a smaller banner with a simple, legible call-to-action in the middle.
***



https://user-images.githubusercontent.com/78797168/131670374-838732fe-79a7-4dc1-9f90-4f35d6b021c0.mp4


### Leaderboard
The leaderboard shows the ten highest-performing fighters, organized by experience spent. If the user isn't logged in, they can still navigate to the pages of the fighters. If the user is logged in, their fighters are highlighted in a unique color. If they have a fighter that is not in the top ten, a separate but identical list shows their place. The top three fighters are gold-, silver- and bronze-colored, respectively.
***



https://user-images.githubusercontent.com/78797168/131670439-3b93ea8a-2a49-4c3b-8ca3-844572e9735f.mp4




### Library
The library is a simple paginated setup with information about currently implemented features and classes. Tabs are controlled by Jinja and kept in separate templates.
***

### Play
The play page is very simple, containing a link to the video on the about page, and the Phaser canvas for playing the game. The phaser canvas will be tested later in this document.
***


https://user-images.githubusercontent.com/78797168/131670449-f7eb240b-8b69-47ca-ae77-349abc8f8ed4.mp4





### Profile
The profile page is where the user is intended to control their account. Here, they can create new characters, access current characters, change email or password, and delete their account. The account deletion is contained in a pop-up modal to prevent accidental deletion. Characters are displayed in a red bar at the head of the page under the account name. The maximum number of characters is 4; with the number controlled by the lack of a "new character" button when 4 characters exist.
***

https://user-images.githubusercontent.com/78797168/131670482-4e3f70ad-32f0-468d-8aea-f02e81beb5e1.mp4


### About
The about page contains some general information about the software, the development team, and a video detailing the complexities of the Phaser canvas and backend games.
***

### Character
The character page is the most complex page next to the play page, weighing in at over 200 lines of JavaScript and 300 lines of html.

It is broken up into four sections:

#### Stats
The stats section contains 10 stats relevant to that character. They are broken up into two sections that stack responsively with each other on smaller screens. Each has its own pop-up tooltip viewable on mouseover.

#### Bio, winrate and icon
The character bio is a scrollable viewing window for the user-entered biography.

The character icon display shows the user-chosen icon. If the character's owner is logged in, a tab underneath the icon expands upon clicking, allowing the user to select a new icon. The icon chosen is updated and changed without refreshing.

Winrate is a simple display of how many matches have been won and lost by the character.

#### Training
Training is split into two sections, each with a textual element and an image representing the tab current accessed in the other element. These two sections allow the user to train various stats relevant to the in-game characteristics of their character, and is reflected in the stat block above.

Extensive JavaScript control moderates what the user sees and does in these windows:
1. Prevents training above the maximum
2. Allows training many levels at once.
3. Shows the cost of each point and the total cost of training.
4. Changes the visible tab when a tab name is clicked on.
5. Changes the associated image to reflect what is being trained.

#### Edit bio and delete character
Edit bio is a simple DB call.

Delete character is hidden behind a button: clicking the delete button opens an in-line dialogue box asking the user to type their character's name, warning them that it is irreversible.
***

### Log in and register
These are separate but equal pages, containing a card with fields for inputting information. Relevant password and email fields have light validation, and the username field will only accept letters and numbers.
***

## Backend Python testing

## Phaser canvas testing
