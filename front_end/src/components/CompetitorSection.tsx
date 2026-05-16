import type { CompanyAnalysisResponse, CompetitorEntry } from "../types";
import { positionLabel, positionTone } from "../utils";

interface CompetitorSectionProps {
  data: CompanyAnalysisResponse;
}

function CompetitorRow({ entry }: { entry: CompetitorEntry }) {
  const tone = positionTone(entry.position);

  return (
    <li className="competitor-row">
      <div>
        <p className="competitor-name">{entry.name}</p>
        <p className="competitor-rationale">{entry.rationale}</p>
      </div>
      <span className={`pill pill-${tone}`}>{positionLabel(entry.position)}</span>
    </li>
  );
}

export default function CompetitorSection({ data }: CompetitorSectionProps) {
  const all = [
    ...data.competitor_analysis.direct_competitors,
    ...data.competitor_analysis.substitutes_or_incumbents,
  ];

  return (
    <section id="competitors" className="detail-card">
      <h3 className="detail-card-title">Competitor analysis</h3>
      <ul className="competitor-list">
        {all.map((entry) => (
          <CompetitorRow key={`${entry.name}-${entry.position}`} entry={entry} />
        ))}
      </ul>
    </section>
  );
}
