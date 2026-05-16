import type { CompanyAnalysisResponse } from "../types";

interface CompanyOverviewSectionProps {
  data: CompanyAnalysisResponse;
  embedded?: boolean;
}

export default function CompanyOverviewSection({
  data,
  embedded = false,
}: CompanyOverviewSectionProps) {
  const o = data.company_overview;
  const foundedHq = [o.founded, o.hq].filter(Boolean).join(" · ");
  const stageRaised = [o.stage, o.total_raised].filter(Boolean).join(" · ");

  const rows: { key: string; value: string }[] = [
    { key: "Problem", value: o.problem_they_solve },
    { key: "Product", value: o.what_they_sell },
    { key: "Buyer", value: o.who_buys_it },
    { key: "Founded · HQ", value: foundedHq || "—" },
    { key: "Stage · Raised", value: stageRaised || "—" },
    { key: "Last round valuation", value: o.last_round_valuation },
    { key: "Headcount", value: o.headcount_trend_linkedin },
  ];

  return (
    <section id="company" className={embedded ? "detail-card-embedded" : "detail-card"}>
      {!embedded ? <h3 className="detail-card-title">Company overview</h3> : null}
      <dl className="kv-list">
        {rows.map((row) => (
          <div key={row.key} className="kv-row">
            <dt className="kv-key">{row.key}</dt>
            <dd className="kv-value">{row.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
