import React from 'react';
import logo from './logo.svg';
import './App.css';
import { ChakraProvider, Flex, Stack, Heading, Text, Button, HStack } from '@chakra-ui/react';
import {chunk, shuffle, State, Options, difficultyColours} from './utils/utils';
import { SEP_9 } from './utils/games';
import useMethods from 'use-methods';

const methods = (state: State) => {
  return {
    toggleActive(item : string) {
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
        state.items = state.incomplete.flatMap((group) => group.items);
        state.activeItems = [];
      } else {
        state.mistakes += 1;
        state.activeItems = [];

        if (state.mistakes === 3) {
          state.complete = [...state.incomplete]
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
    mistakes: 0
  };

  const [state, finish] = useMethods(methods, initState);

  return {
    ...state,
    ...finish
  };
};

function App() {
  const game = useGame({
    groups: SEP_9
  })
  return (
    <ChakraProvider>
      <Flex h ='100vh' w = '100vw' align = 'center' justify='center'>
        <Stack spacing={4}>
          <Heading>
            Premier League Connections!
          </Heading>
          <Text>Can you pick the four premier league players with something in common?</Text>
          <Stack>
            {game.complete.map((group) => (
              <Stack className='done-group' bg={difficultyColours(group.difficulty)}>
                <Text className='done-category'>{group.category}</Text>
                <Text className='done-items'>{group.items.join(',')}</Text>
              </Stack>
            ))}
            
          {chunk(game.items, 4).map((row) => (
            <>
              <HStack>
                {row.map((item) => (
                  <Button className='item-button' _active={{ bg:'#48454d', color:'white' }} onClick={() => game.toggleActive(item)} isActive={game.activeItems.includes(item)}>
                    {item}
                  </Button>
              ))}
              </HStack>
            </>
          ))}
          </Stack>

        <HStack align='baseline'>
          <Text> Mistakes Made: {game.mistakes}</Text>
        </HStack>
        <HStack spacing={4}>
          <Button className='action-button' onClick={game.shuffle}>
            Shuffle
          </Button>
          <Button className='action-button' onClick={game.deselectAll}>
            Deselect All
          </Button>
          <Button className='action-button' onClick={game.submit}>
            Submit
          </Button>
        </HStack>
      </Stack>
      </Flex>
    </ChakraProvider>

  );
}

export default App;
