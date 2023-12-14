## Flove Blog

[Flove](https://favourolumese.pythonanywhere.com/articles/) is a rich text editor blog with text-to-speech functionality built using the Django framework. It leverages the Gravatar API for default images and allows users to log in with email or username. The platform includes user verification via email, along with liking, commenting, bookmarking, and RSS feed capabilities.

## Functionalities and Use Cases

**Article Creation:**

* Users can create drafts, public, or unlisted articles.
* Public articles are visible to everyone, while unlisted articles require sharing the link for viewing.
* Drafts are only accessible to the author.

**Gravatar API:**

* Used for fetching default images when users opt out of uploading their profile pictures.

**Pyttsx3:**

* Generates audio for each article, stored as a file in the database.

**CKEditor:**

* Powers the rich text editor, enabling users to add images and links to their articles.

**django-cleanup:**

* Automatically deletes associated media files when an article or user account is deleted.

**Email Verification and Notification:**

* Account verification is mandatory before login.
* Unsuccessful login attempts by unverified users trigger a resend verification email.
* Authors receive notifications for article comments, and commenters receive notifications for replies.

**django-social-share:**

* Enables easy sharing of articles across various social media platforms.
* Allows users to copy article links to the clipboard.

**RSS Functionality**

* The blog includes RSS functionality for each author.

**Database:**

* PostgreSQL for development.
* MySQL for production.

**Web and Application Servers:**

* Development: Gunicorn (web) and Nginx (application).
* PythonAnywhere: Uwsgi (web) and Nginx (application) (default and unchangeable).

## Technologies Used

* Django
* jQuery
* JavaScript
* HTML
* CSS

## Possible Improvements

* **SMTP Provider:** Consider exploring alternative SMTP providers, as occasional errors or delays in message delivery have been observed with Gmail.
* **Article Saving:** Implement the ability to save/unsave an article directly from the article list or writer's page.
* **Bookmarking Unlisted Articles:** Unlisted articles are bookmarkable and public articles converted to unlisted are still bookmarked though not visible.
* Consider making unlisted articles un-bookmarkable and public articles made unlisted unbookmarked
