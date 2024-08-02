"use client";
import { Card, CardContent, Typography } from '@mui/material';

interface Cocktail {
  name: string;
  description: string;
  ingredients: string;
  garnish: string;
  glassware: string;
  preparation: string;
  notes: string;
  location: string;
  bar_company: string;
  bartender: string;
}

interface Props {
  results: Cocktail[];
}

export const SearchResults: React.FC<Props> = ({ results }) => {
  return (
    <>
      {results.map((cocktail, index) => (
        <Card key={index} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h5">{cocktail.name}</Typography>
            <Typography variant="body2">{cocktail.description}</Typography>
            <Typography variant="body2">{cocktail.ingredients}</Typography>
{/*
    #         'garnish': cocktail.garnish,
    #         'glassware': cocktail.glassware,
    #         'preparation': cocktail.preparation,
    #         'notes': cocktail.notes,
    #         'location': cocktail.location,
    #         'bar_company': cocktail.bar_company,
    #         'bartender': cocktail.bartender
      */}
          </CardContent>
        </Card>
      ))}
    </>
  );
};
