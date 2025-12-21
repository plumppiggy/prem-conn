import './App.css';
import './anim.css';
import { ChakraProvider, Flex, Stack, Heading, Text, Button, HStack, Box, IconButton, Modal} from '@chakra-ui/react';
import {chunk, shuffle, State, Options, difficultyColours} from './utils/utils';
import { SEP_9, SEP_12, SEP_13, SEP_14, SEP_15, SEP_16, SEP_17, SEP_18, test, SEP_21, SEP_22, SEP_24, test2} from './utils/games';
import useMethods from "./hooks/useMethods";
import {TbRectangleVerticalFilled} from 'react-icons/tb'
import {BsFillPersonFill, BsTicket} from 'react-icons/bs'
import HowToPlay from './components/HowToPlay';
import {GiSoccerBall} from 'react-icons/gi'
import premLogo from './fpl.png'
import { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Homepage from './components/homepage';
import ConnectionsGame from './components/connections/connections';
import CrosswordPage from './components/crossword/crosswordPage';


function App() {

  


  return (
    <ChakraProvider>
      <BrowserRouter basename='/prem-conn'>
      <Routes>
        <Route path='/' element={<Homepage />}>
        <Route path='connections' element={<ConnectionsGame />} />
        <Route path='crossword' element={<CrosswordPage />} />
        </Route>
      </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
