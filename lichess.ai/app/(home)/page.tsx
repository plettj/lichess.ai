import { Button } from "@/components/ui/button";

export default async function Home() {
  return (
    <main className="flex flex-col gap-2 my-auto items-center">
      <h1>Lichess.ai</h1>
      <p>A little data analysis website.</p>
      <hr className="h-2" />
      <Button asChild className="w-64 my-2">
        <a
          target="_blank"
          href="https://kurser.dtu.dk/course/02450"
          rel="noopener noreferrer"
        >
          Data
        </a>
      </Button>
    </main>
  );
}
