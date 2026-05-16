import type { CompanyAnalysisResponse } from "../types";
import { verdictTone } from "../utils";

interface InvestmentSectionProps {
  data: CompanyAnalysisResponse;
}

export default function InvestmentSection({ data }: InvestmentSectionProps) {
  const { investment_recommendation: rec, company_name } = data;
  const tone = verdictTone(rec.verdict);
  const valueClass =
    tone === "positive"
      ? "metric-value-positive"
      : tone === "negative"
        ? "metric-value-negative"
        : "metric-value-neutral";

  return (
    <section id="investment" className="report-block">
      <div className="report-header">
        <h2 className="report-title">
          Investment recommendation — {company_name}
        </h2>
        <span className={`badge badge-${tone}`}>{rec.verdict}</span>
      </div>

      <div className="metrics-row">
        <div className="metric-card">
          <p className={`metric-value ${valueClass}`}>{rec.confidence_score}</p>
          <p className="metric-label">Confidence (0–100)</p>
        </div>
        <div className="metric-card">
          <p className={`metric-value ${valueClass}`}>{rec.verdict}</p>
          <p className="metric-label">Verdict</p>
        </div>
      </div>

      <div className="detail-card detail-card-full">
        <h3 className="detail-card-title">Confidence reasoning</h3>
        <div className="reasoning-block">
          <h4 className="subsection-title">What moves it up</h4>
          <ul className="bullet-list">
            {rec.confidence_reasoning.what_moves_it_up.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="reasoning-block">
          <h4 className="subsection-title">What moves it down</h4>
          <ul className="bullet-list">
            {rec.confidence_reasoning.what_moves_it_down.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
