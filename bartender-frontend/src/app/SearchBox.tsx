"use client";
import { Button, TextField, Box } from '@mui/material';
import { useState } from 'react';

interface Props {
  onSearch: (query: string) => void;
}

export const SearchBox: React.FC<Props> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <Box sx={{ display: 'flex', gap: 1 }}>
      <TextField
        label="Search Cocktails"
        variant="outlined"
        fullWidth
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
      />
      <Button variant="contained" onClick={handleSearch}>Search</Button>
    </Box>
  );
};
