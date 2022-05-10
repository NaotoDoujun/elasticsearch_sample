
import { SearchProvider, Results, ErrorBoundary, Paging } from '@elastic/react-search-ui';
import { SearchAppBar } from '../Common'
import { WIKIPEDIA_CONFIG, NATIONAL_PARKS_CONFIG } from '../../SearchConfigs'

function Home() {
  return (
    // <SearchProvider config={NATIONAL_PARKS_CONFIG}>
    //   <SearchAppBar />
    //   <ErrorBoundary>
    //     <Results titleField="title"
    //       urlField="nps_link"
    //       thumbnailField="image_url"
    //       shouldTrackClickThrough={true} />
    //     <Paging />
    //   </ErrorBoundary>
    // </SearchProvider>
    <SearchProvider config={WIKIPEDIA_CONFIG}>
      <SearchAppBar />
      <ErrorBoundary>
        <Results titleField="title" shouldTrackClickThrough={true} />
        <Paging />
      </ErrorBoundary>
    </SearchProvider>
  )
}

export { Home }