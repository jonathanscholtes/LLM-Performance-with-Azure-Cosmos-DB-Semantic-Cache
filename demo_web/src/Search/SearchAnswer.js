import React from 'react'

import { Box, Paper, Stack, Typography } from '@mui/material'

export default function SearchAnswer(results) {
  return (
    <Paper sx={{ p: 2 }}>
      <Stack direction="column" spacing={2} useFlexGap flexWrap="wrap">
        <Typography
          variant="subtitle1"
          sx={{ color: 'grey', fontSize: '12pt' }}
        >
          Answer:
        </Typography>
        <Box
          sx={{
            border: 1,
            borderColor: 'lightgray',
            borderRadius: 3,
            p: 1,
            fontSize: 14,
          }}
        >
          {results.results.text}
        </Box>
        
        <Stack>
          <Typography
          variant="caption"
          sx={{ color: 'grey', fontSize: '10pt' }}
          >
            Response Time (seconds)
          </Typography>
          <Typography
          variant="caption"
          sx={{ color: 'grey', fontSize: '10pt' }}
          >
            {results.results.ResponseSeconds}
            </Typography>
        </Stack>
      </Stack>
    </Paper>
  )
}
