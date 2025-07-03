type PageProps = {
  pageNumber: number;
  content: string;
};

export default function Page({ pageNumber, content }: PageProps) {
  return (
    <div className="bg-white dark:bg-[#111] overflow-hidden shadow-lg rounded- p-6 mb-10 border border-muted w-full max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-4 text-muted-foreground text-xs">
        <span>Page {pageNumber}</span>
        <span>•••</span> {/* Optional for decoration */}
      </div>
      <div className="text-lg whitespace-pre-line leading-relaxed font-serif text-gray-800 dark:text-gray-400">
        {content}
      </div>
    </div>
  );
}
