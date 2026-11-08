# Translation prompt (run in a new, clean window)

The READJH window that wrote the native-language README does not translate.
After the user approves that README, open a new, clean window, paste this
prompt, and fill in the four values below. Run the job there.

## Fill these in first

- **Native language:** `<language of the approved README>`
- **Native README:** `<path to the approved README>`
- **Translate to:** `<target language; one per file when they differ>`
- **Files to translate:** `<one path per line; create the file if it does not exist, otherwise correct it>`

Read the native README in full before writing anything.

## Rules

1. **Native first.** Read the native README section by section, then translate
   from it. Do not translate from another translated README.
2. **One-to-one structure.** Keep one chapter to one chapter and one paragraph
   to one paragraph. Do not merge, split, add, or drop sections. Keep headings,
   list order, tables, and code block order in the same place.
3. **Ask when a term has no good equivalent.** When a term has no natural word
   in the target language, stop and ask the author which word to use. Do not
   invent a new compound word or keep an English word without asking.
4. **No jargon and no translationese.** Use the words people actually say in
   the target language. Do not carry English sentence bones into the
   translation.
5. **Keep facts fixed.** Do not change code, commands, links, versions,
   numbers, badges, file paths, or direct quotes. Copy them byte for byte.
   If a target file states a different fact, stop and report it to the author
   instead of fixing it here.
6. **New clean window only.** This job runs in the new window, never in the
   window that wrote the native README. Do not go back to that window to
   translate.
7. **Natural native wording.** Translate and correct the target README's
   existing text so it reads like a person wrote it in the target language.
   Do not use made-up complex words.
8. **Return a correspondence table.** List each section and paragraph with its
   source and target text, and mark every term that has no exact equivalent.

## Finish

When the translation is done, report the files changed and the correspondence
table. If a term question is still open, leave it in the table and in your
final message.
