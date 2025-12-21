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

const methods = (state: State) => {
  return {
    toggleActive(item : string) {
      state.wiggleItems = [];
      if (state.activeItems.includes(item)) {
        state.activeItems = state.activeItems.filter(i => i !== item);
      } else if (state.activeItems.length < 4) {
        state.activeItems.push(item);
      }
    },

    shuffle() {
      shuffle(state.items);
    },

    deselectAll() {
      state.activeItems = [];
    },

    submit() {
      const correctGroup = state.incomplete.find ((group) => 
        group.items.every((item) => state.activeItems.includes(item)),
      );

      

      if (correctGroup) {
        // take the actions with the correct group
        state.complete.push(correctGroup);
        state.incomplete = state.incomplete.filter((item) => item !== correctGroup);
        state.items = state.items.filter((item) => !correctGroup.items.includes(item));
        state.activeItems = [];
      } else {
        // TODO: Make the wiggle animation
        state.wiggleItems = state.activeItems;
        state.mistakes += 1;
        state.activeItems = [];

        if (state.mistakes === 3) {
          state.complete = state.complete.concat(state.incomplete);
          state.incomplete = [];
          state.items = [];
        }
      }
    }
  }
}

const useGame = (options: Options) => {
  const initState: State = {
    incomplete: options.groups,
    complete: [],
    items: shuffle(options.groups.flatMap((g) => g.items)),
    activeItems: [],
    mistakes: 0,
    wiggleItems: [],
    oneAway: false
  };

  const [state, finish] = useMethods(methods, initState);

  return {
    ...state,
    ...finish
  };
};

function App() {

  const [oneAway, setOneAway] = useState(false)
  
  const game = useGame({
    groups: test2
  })

  const date = new Date(Date.now()).toDateString()

  function submitSelection() {
    game.submit()
    const oneAway = game.incomplete.find((group) => group.items.filter(o => game.activeItems.includes(o)).length == 3)
    
    if (oneAway) {
      setOneAway(true)
      setTimeout( () => setOneAway(false), 2000)
    }

  }


  return (
    <ChakraProvider>
      <BrowserRouter basename='/prem-conn'>
      <Routes>
        <Route path='/' element={<Homepage />}>
        <Route path='connections' element={<ConnectionsGame />} />
        </Route>
      </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
