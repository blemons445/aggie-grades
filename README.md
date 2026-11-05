# Aggie Grade Finder

A faster, sortable way to look up Texas A&M grade distributions by course or professor.

- `index.html` is the whole site. Ten courses are bundled so it opens instantly.
- `api/grades.js` is a Vercel serverless function. Type any course (e.g. `BUSN 489`) and the page calls `/api/grades?dept=BUSN&number=489` to load it. Responses are cached for a day at Vercel's edge.

## Deploy

1. Push this folder to a GitHub repo.
2. On vercel.com, choose **Add New → Project**, import the repo, and click **Deploy**. No build settings needed.
3. Every push to `main` redeploys.

## Data

Section-level grade counts come from Texas A&M's public grade distribution reports, via anex.us. Professors appear as last name plus first initial, as in the reports. Syllabus and review links point to Howdy's public class search and Rate My Professors.
