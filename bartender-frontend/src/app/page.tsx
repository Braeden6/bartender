"use client";
import { Container, Typography } from '@mui/material';
import type { NextPage } from 'next';
import { useState } from 'react';
import { SearchBox } from '../app/SearchBox';
import { SearchResults } from '../app/SearchResults';

const Home: NextPage = () => {
  const [results, setResults] = useState([]);

  const handleSearch = async (query: string) => {
    const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    setResults(data);
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Cocktail Search
      </Typography>
      <SearchBox onSearch={handleSearch} />
      <SearchResults results={results} />
    </Container>
  );
};

export default Home;
