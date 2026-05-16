import type { CompanyAnalysisResponse } from "../types";

interface FounderQuestionsSectionProps {
  data: CompanyAnalysisResponse;
}

function buildQuestions(data: CompanyAnalysisResponse): string[] {
  const { company_name, investment_recommendation: rec } = data;

  return [
    `What evidence do you have that ${company_name}'s buyers will pay at venture-scale pricing for what you sell?`,
    `How does your differentiation hold against incumbents when the verdict is ${rec.verdict} at ${rec.confidence_score}/100 confidence?`,
    `What single execution milestone in the next 12 months would most change your ${rec.verdict} view — and what happens if you miss it?`,
  ];
}

export default function FounderQuestionsSection({
  data,
}: FounderQuestionsSectionProps) {
  const questions = buildQuestions(data);

  return (
    <section id="founder-questions" className="detail-card detail-card-full">
      <h3 className="detail-card-title">3 sharpest founder questions</h3>
      <ol className="founder-questions">
        {questions.map((q) => (
          <li key={q}>{q}</li>
        ))}
      </ol>
    </section>
  );
}
