import { Results, ErrorBoundary, PagingInfo, Paging } from '@elastic/react-search-ui';

function NewsResults() {
  return (
    <ErrorBoundary>
      <PagingInfo />
      <Results titleField="title" />
      <Paging />
    </ErrorBoundary>
  )
}

export { NewsResults }