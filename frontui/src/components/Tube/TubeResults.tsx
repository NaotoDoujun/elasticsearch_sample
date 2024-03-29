import * as React from 'react';
import { Results, ErrorBoundary, PagingInfo, Paging } from '@elastic/react-search-ui';
import { SearchResult } from '@elastic/search-ui';
import { Grid, Typography, Link, ButtonBase } from '@mui/material';
import { styled } from '@mui/material/styles';

const Img = styled('img')({
  margin: 'auto',
  display: 'block',
  maxWidth: '100%',
  maxHeight: '100%',
});

function TubeResults() {

  const getFieldType = (result: SearchResult, field: string, type: string) => {
    if (result[field]) return result[field][type];
  }

  const getRaw = (result: SearchResult, field: string) => {
    return getFieldType(result, field, "raw");
  }

  const getSnippet = (result: SearchResult, field: string) => {
    return getFieldType(result, field, "snippet");
  }

  const htmlEscape = (str: string) => {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  const getEscapedField = (result: SearchResult, field: string) => {
    const safeField =
      getSnippet(result, field) || htmlEscape(getRaw(result, field));
    return Array.isArray(safeField) ? safeField.join(", ") : safeField;
  }

  return (
    <ErrorBoundary>
      <PagingInfo />
      <Results resultView={({ result, onClickLink }) => {
        const title = getEscapedField(result, "title");
        const text = getEscapedField(result, "text");
        return (
          <Grid container component="li" onClick={onClickLink} sx={{ p: 1, borderBottom: 1, borderColor: 'divider' }}>
            <Grid item md={2}>
              <ButtonBase sx={{ height: 150 }} href={result.url.raw} target="_blank" rel="noopener">
                <Img alt="thumbnail" src={result.thumbnail.raw} />
              </ButtonBase>
            </Grid>
            <Grid item md={10} sx={{ px: 2 }}>
              <Typography variant="h6" dangerouslySetInnerHTML={{ __html: title }} />
              <Typography variant="subtitle2">{result.time.raw}</Typography>
              <Typography component="div" variant="body2" dangerouslySetInnerHTML={{ __html: text }} />
              <Link href={result.url.raw} target="_blank" rel="noopener">{result.url.raw}</Link>
            </Grid>
          </Grid>
        );
      }} />
      <Paging />
    </ErrorBoundary>
  )
}

export { TubeResults }