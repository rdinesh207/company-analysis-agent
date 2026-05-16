import { FormEvent, useState } from "react";
import { analyzeCompany } from "../api";
import type { CompanyAnalysisResponse, MemoSectionId } from "../types";
import { scrollToSection } from "../utils";
import MemoGrid from "./MemoGrid";
import AnalysisReport from "./AnalysisReport";

export default function LandingPage() {
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompanyAnalysisResponse | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const name = companyName.trim();
    if (!name) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeCompany({ company_name: name });
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
          Type a company name. The agent returns a structured investment memo
          your team would otherwise spend two days assembling — in the same
          shape, every time, for every deal.
        </p>

        <section className="io-panel" aria-label="Input and memo preview">
          <div className="io-input-wrap">
            <p className="io-label">Input</p>
            <form className="io-form" onSubmit={handleSubmit}>
              <input
                className="io-input"
                type="text"
                placeholder="Enter company name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                disabled={loading}
                aria-label="Company name"
              />
              <p className="io-hint">e.g. &apos;Cursor&apos;, &apos;Ramp&apos;, &apos;Hightouch&apos;</p>
              <button className="io-submit" type="submit" disabled={loading || !companyName.trim()}>
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
                  : "Submit a company name to preview memo sections"}
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
