import { Button } from "@/components/ui/button";
import { GitHubLogoIcon } from "@radix-ui/react-icons";
import Link from "next/link";

export default async function Home() {
  return (
    <main className="flex flex-col gap-6 my-auto items-center">
      <h1 className="font-bold">Lichess.ai</h1>
      <p>
        A{" "}
        <a
          className="no-underline text-blue-900 hover:to-blue-700 hover:underline"
          href="https://database.lichess.org/#standard_games"
        >
          lichess database
        </a>{" "}
        data analysis and machine learning project.
      </p>
      <p>
        Built by{" "}
        <a
          className="no-underline text-blue-900 hover:to-blue-700 hover:underline"
          href="https://plett.dev"
        >
          Josiah
        </a>
        ,{" "}
        <a
          className="no-underline text-blue-900 hover:to-blue-700 hover:underline"
          href="https://tdude92.github.io/"
        >
          Trevor
        </a>
        , and{" "}
        <a
          className="no-underline text-blue-900 hover:to-blue-700 hover:underline"
          href="https://www.linkedin.com/in/tonglei-liu-18291a248/"
        >
          Tonglei
        </a>
        .
      </p>
      <Button asChild>
        <Link href="https://github.com/plettj/lichess.ai">
          <GitHubLogoIcon className="mr-2" /> Code
        </Link>
      </Button>
      <Button asChild variant="outline">
        <Link href="/static/reports/feature-extraction-and-visualization.pdf">
          Report 1 - Feature Extraction and Visualization
        </Link>
      </Button>
      <Button asChild variant="outline">
        <Link href="/static/reports/supervised-learning-classification-and-regression.pdf">
          Report 2 - Supervised Learning, Classification, and Regression
        </Link>
      </Button>
      <Button asChild variant="outline">
        <a
          target="_blank"
          href="https://kurser.dtu.dk/course/02450"
          rel="noopener noreferrer"
        >
          Course Link
        </a>
      </Button>
    </main>
  );
}
