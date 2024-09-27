import { Button } from "@/components/ui/button";

export default async function Home() {
  return (
    <main className="flex flex-col gap-2 my-auto items-center">
      <h1>Lichess.ai</h1>
      <p>
        A{" "}
        <a
          className="no-underline text-blue-900 hover:to-blue-700"
          href="https://database.lichess.org/#standard_games"
        >
          lichess database
        </a>{" "}
        data analysis website.
      </p>
      <hr className="h-2" />
      <Button asChild className="w-64 my-2">
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
