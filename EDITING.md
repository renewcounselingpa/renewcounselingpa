# How to change the words on the website

You don't need to know anything about GitHub or code. All the text on the website lives in **one file, `content.txt`**, and you can edit it in your web browser.

## Steps

1. Go to the repository page on GitHub and sign in. [Visit the repo](https://github.com/renewcounselingpa/renewcounselingpa/tree/main)
2. Click the file **`content.txt`**. [Visit content.txt](https://github.com/renewcounselingpa/renewcounselingpa/blob/main/content.txt)
3. Click the **pencil icon** (✏️, "Edit this file") at the top right of the file.
4. Find the text you want to change. Use **Ctrl+F** (Windows) or **Cmd+F** (Mac) to search for a few of the words.
5. Change the text. **Only change what comes after the first colon.** Leave the name before the colon alone.

   ```
   hero_title: Room to grow, at your own pace.
   ^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   leave this        change this part
   ```
6. Click the green **Commit changes…** button at the top right, then **Commit changes** again in the box that appears. It'll ask you for a message, which you can change or leave as default.
7. Wait **1–3 minutes**. The website updates by itself. Reload the page (Ctrl/Cmd+Shift+R) to see it.

## Things you can do

| To… | Do this |
|---|---|
| Change the phone number, email, address, fees, or "years in practice" | Edit it once in the **SETTINGS** section at the top. It updates everywhere it appears. |
| Add an item to a list (a tag, a credential, an insurance plan) | Copy a line beginning with `- ` in that list and change the text. |
| Remove a list item | Delete its line. |
| Make words **bold** | Put two stars around them: `**like this**` |
| Add a link | `[the words people click](https://example.com)` |
| Hide "Accepting new clients" | Set `accepting_clients: no` |
| Leave yourself a note | Start a line with `#`. It never appears on the site. |

## If something goes wrong

- **Made a mistake you can't undo?** Open `content.txt`, click **History** (top right), pick an earlier version, and copy its text back.
- **Site didn't change after a few minutes?** Click the **Actions** tab on GitHub ([here](https://github.com/renewcounselingpa/renewcounselingpa/actions)). A red ✗ next to your change means a line in `content.txt` isn't written correctly. Click it to see which line and what's wrong, then fix that line. The live site keeps showing the old version until it's fixed, so it can't break.
- Every line must look like `name: text` (with the colon). Lists are `- item` lines directly under a name with nothing after the colon.

## What's *not* in `content.txt`

Photos (replace the file in the `images/` folder, keeping the same filename), colors and layout (`css/styles.css`), and small labels like the contact form's field names. Ask whoever maintains the site for those.
