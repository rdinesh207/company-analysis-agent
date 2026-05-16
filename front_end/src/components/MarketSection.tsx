import type { CompanyAnalysisResponse } from "../types";

interface MarketSectionProps {
  data: CompanyAnalysisResponse;
}

export default function MarketSection({ data }: MarketSectionProps) {
  const m = data.market_analysis;

  return (
    <section id="market" className="detail-card">
      <h3 className="detail-card-title">Market analysis</h3>
      <article className="subsection">
        <h4 className="subsection-title">Why the problem matters</h4>
        <p className="subsection-body">{m.why_problem_matters}</p>
      </article>
      <article className="subsection">
        <h4 className="subsection-title">Why now</h4>
        <p className="subsection-body">{m.why_now}</p>
      </article>
      <article className="subsection">
        <h4 className="subsection-title">What changed in 24 months</h4>
        <ul className="bullet-list">
          {m.recent_changes_last_24_months.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </article>
    </section>
  );
}
