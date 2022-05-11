
import { Results, ErrorBoundary, Paging } from '@elastic/react-search-ui';

function Home() {
  return (
    <ErrorBoundary>
      <Results titleField="title" shouldTrackClickThrough={true} />
      <Paging />
    </ErrorBoundary>
  )
}

export { Home }