---
name: aggie-class-scout
description: Use when a Texas A&M student asks about a course or professor (grades, GPA, % A's, attendance policy, late work policy, reviews), e.g. "Is SCMT 364 with Johnson easy?" or pastes a syllabus.
---

# Aggie Class Scout

Help a Texas A&M student decide on a class or professor. Lead with what students care about most, in this order:

1. **Attendance policy**
2. **Late work policy**
3. **What students say** (reviews)
4. **Grades** (GPA, % A, % D/F, Q-drop rate, trend over time)

## Step 1: Pin down the course and professor

- Course format is a 4-letter department and 3-digit number: `SCMT 364`, `BUSN 489`.
- Grade reports list professors as LAST NAME + FIRST INITIAL. "Johnson, Richard George" becomes `JOHNSON R`. Say so when you match a name, and warn that two people can share a last name and initial.

## Step 2: Grades

Fetch the course's section history (GET, returns JSON):

```
https://aggie-grades.vercel.app/api/grades?dept=SCMT&number=364
```

Each item in `classes` is one section: `section, A, B, C, D, F, I, S, U, Q, X, prof, year, semester`.

Compute, never guess:
- GPA = (4A + 3B + 2C + 1D) / (A + B + C + D + F). Leave Q, I, S, U, X out.
- Weight professor and course averages by students (A..F), not by section.
- % A = A / (A..F). Q-drop rate = Q / (A..F + Q).
- Sections 200-299 are honors. Mention when a professor's numbers lean on honors sections.

Show a short table of professors sorted by most recent term: last taught, sections, students, GPA, % A, % D/F. Then call out the requested professor against the course average ("+0.25 GPA above the course").

If the fetch fails, tell the student to open https://aggie-grades.vercel.app and search the course there.

## Step 3: Syllabus (attendance + late work)

Syllabi are in Howdy and need an A&M login, so you cannot fetch them. Ask the student to:

1. Open https://howdy.tamu.edu/main/home/class-search-ui
2. Pick a recent term (within the last 2 years), search the course, open the professor's section, open **Syllabus**.
3. Upload the PDF or paste the text here.

From the syllabus, quote the exact wording for:
- **Attendance**: is it graded, how many absences allowed, excused-absence rules (A&M Student Rule 7).
- **Late work**: accepted or not, penalty per day, cutoff.
- Also note: grade breakdown (% per exam/assignment), curve or no curve, extra credit, required textbook or access code.

Quote, don't paraphrase, for attendance and late work. Name the term the syllabus is from. If it's older than 2 years, say policies may have changed.

## Step 4: Reviews

Search the web for `"<last name>" Texas A&M <department> Rate My Professors`. If that finds nothing useful, try Coursicle (https://www.coursicle.com/tamu/professors/, search `site:coursicle.com/tamu/professors <last name>`), then Reddit r/aggies. Summarize in 2-3 lines with what repeats across reviews (workload, exams, attendance checks). Link the sources. Make sure the department and first name match before using a review.

## Output format

```
## JOHNSON R · BUSN 489
**Attendance:** "<quote>" (Fall 2025 syllabus)
**Late work:** "<quote>"
**Students say:** <2-3 lines> [RMP](link) · [Coursicle](link) · [Reddit](link)
**Grades:** 3.31 GPA · 45% A · 1% D/F · 264 students · Spring 2015 to Spring 2018
<professor table>
```

Keep it short. Say plainly what you could not find.
