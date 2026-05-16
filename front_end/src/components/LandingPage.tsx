import { FormEvent, useState } from "react";
import { analyzeCompany } from "../api";
import type { CompanyAnalysisResponse, MemoSectionId } from "../types";
import { normalizeWebsite, scrollToSection } from "../utils";
import MemoGrid from "./MemoGrid";
import AnalysisReport from "./AnalysisReport";

export default function LandingPage() {
  const [companyName, setCompanyName] = useState("");
  const [companyWebsite, setCompanyWebsite] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompanyAnalysisResponse | null>(null);

  const canSubmit =
    !loading && companyName.trim().length > 0 && companyWebsite.trim().length > 0;

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const name = companyName.trim();
    const website = normalizeWebsite(companyWebsite);
    if (!name || !website) {
      setError("Enter a company name and a website URL.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeCompany({
        company_name: name,
        company_website: website,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleCardSelect(sectionId: MemoSectionId) {
    scrollToSection(sectionId);
  }

  return (
    <main className="page">
      <div className="page-inner">
        <p className="section-label">
          <span className="section-label-num">02</span>
          <span>What it is</span>
        </p>

        <h1 className="hero-title">
          A company analysis agent. One input. One memo.
        </h1>
        <div className="hero-accent-line" aria-hidden />
        <p className="hero-description">
          Type a company name and its website. The agent returns a structured
          investment memo your team would otherwise spend two days assembling —
          in the same shape, every time, for every deal.
        </p>

        <section className="io-panel" aria-label="Input and memo preview">
          <div className="io-input-wrap">
            <p className="io-label">Input</p>
            <form className="io-form" onSubmit={handleSubmit}>
              <div className="io-input-row">
                <input
                  className="io-input"
                  type="text"
                  placeholder="Company name"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  disabled={loading}
                  aria-label="Company name"
                />
                <input
                  className="io-input"
                  type="text"
                  placeholder="Website (e.g. cursor.com)"
                  value={companyWebsite}
                  onChange={(e) => setCompanyWebsite(e.target.value)}
                  disabled={loading}
                  aria-label="Company website"
                  inputMode="url"
                />
              </div>
              <p className="io-hint">
                e.g. &apos;Cursor&apos; · cursor.com — both fields required
              </p>
              <button className="io-submit" type="submit" disabled={!canSubmit}>
                {loading ? "Analyzing…" : "Generate memo"}
              </button>
            </form>
          </div>

          <div className="io-arrow" aria-hidden>
            →
          </div>

          <div>
            <p className="io-label">Output — structured memo</p>
            {result ? (
              <MemoGrid onSelect={handleCardSelect} />
            ) : (
              <div className="io-output-placeholder">
                {loading
                  ? "Building structured memo…"
                  : "Submit a company name and website to preview memo sections"}
              </div>
            )}
          </div>
        </section>

        {error ? <p className="error-banner" role="alert">{error}</p> : null}

        {result ? <AnalysisReport data={result} /> : null}
      </div>
    </main>
  );
}
