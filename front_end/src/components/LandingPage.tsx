import { FormEvent, useState } from "react";
import { analyzeCompany } from "../api";
import type { CompanyAnalysisResponse } from "../types";
import AnalysisReport from "./AnalysisReport";

export default function LandingPage() {
  const [companyName, setCompanyName] = useState("");
  const [companyUrl, setCompanyUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompanyAnalysisResponse | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const name = companyName.trim();
    const url = companyUrl.trim();
    if (!name) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeCompany({
        company_name: name,
        ...(url ? { company_website: url } : {}),
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
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
        <div className="hero-accent-line" aria-hidden="true" />
        <p className="hero-description">
          Type a company name and its website. The agent returns a structured
          investment memo your team would otherwise spend two days assembling —
          in the same shape, every time, for every deal.
        </p>

        <section className="io-panel" aria-label="Company input">
          <p className="io-label">Input</p>
          <form className="io-form" onSubmit={handleSubmit}>
            <div className="io-field">
              <label className="io-field-label" htmlFor="company-name">
                Company name
              </label>
              <input
                id="company-name"
                className="io-input"
                type="text"
                placeholder="Enter company name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                disabled={loading}
              />
            </div>
            <div className="io-field">
              <label className="io-field-label" htmlFor="company-url">
                Company URL
              </label>
              <input
                id="company-url"
                className="io-input"
                type="url"
                placeholder="https://example.com"
                value={companyUrl}
                onChange={(e) => setCompanyUrl(e.target.value)}
                disabled={loading}
              />
            </div>
            <p className="io-hint">e.g. &apos;Cursor&apos;, &apos;Ramp&apos; · https://stripe.com/</p>
            <div className="io-actions">
              <button className="io-submit" type="submit" disabled={loading || !companyName.trim()}>
                {loading ? "Analyzing…" : "Generate memo"}
              </button>
            </div>
          </form>
        </section>

        {error ? <p className="error-banner" role="alert">{error}</p> : null}

        {result ? <AnalysisReport data={result} /> : null}
      </div>
    </main>
  );
}
