// Looks up one course's section-level grade history and caches it at Vercel's edge for a day.
// Source: anex.us, which compiles Texas A&M's public grade distribution reports.
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  const dept = String(req.query.dept || "").trim().toUpperCase();
  const number = String(req.query.number || "").trim();
  if (!/^[A-Z]{4}$/.test(dept) || !/^\d{3}$/.test(number)) {
    res.status(400).json({ error: "Use a 4-letter department and 3-digit number, e.g. dept=SCMT&number=364" });
    return;
  }
  try {
    const r = await fetch("https://anex.us/grades/getData/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "aggie-grade-finder" },
      body: new URLSearchParams({ dept, number }).toString(),
    });
    if (!r.ok) throw new Error("upstream " + r.status);
    const data = JSON.parse(await r.text());
    res.setHeader("Cache-Control", "public, s-maxage=86400, stale-while-revalidate=604800");
    res.status(200).json({ classes: Array.isArray(data.classes) ? data.classes : [] });
  } catch (e) {
    res.status(502).json({ error: "Could not reach the grade data source. Try again in a minute." });
  }
};
