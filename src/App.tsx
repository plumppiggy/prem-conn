import './App.css';
import './anim.css';
import { ChakraProvider, Flex, Stack, Heading, Text, Button, HStack, Box, IconButton} from '@chakra-ui/react';
import {chunk, shuffle, State, Options, difficultyColours} from './utils/utils';
import { SEP_9, SEP_12, SEP_13, SEP_14, SEP_15, SEP_16, SEP_17, SEP_18} from './utils/games';
import useMethods from 'use-methods';
import {TbRectangleVerticalFilled} from 'react-icons/tb'
import {BsFillPersonFill} from 'react-icons/bs'
import HowToPlay from './components/HowToPlay';
import {GiSoccerBall} from 'react-icons/gi'
import premLogo from './fpl.png'

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
    wiggleItems: []
  };

  const [state, finish] = useMethods(methods, initState);

  return {
    ...state,
    ...finish
  };
};

function App() {
  const game = useGame({
    groups: SEP_18
  })
  return (
    <>
    <ChakraProvider>
      <Flex h ='100%' w = '100%' align = 'center' justify='center' style={{padding:'1vh'}}>
        <Stack spacing={4}>
          <HStack>
            <Heading>
              Premier League Connections!
            </Heading>
            <img height='80px' width='60px' src={premLogo}/>
          </HStack>
          
          <HStack>
            <Text>Can you pick the four premier league players with something in common?</Text>
            <HowToPlay/>
            <a href='https://fantasy.premierleague.com/entry/5880685/event/4/'>
              <IconButton aria-label='fpl team' icon={<GiSoccerBall/>} />
            </a>
          </HStack>
          

          <Stack style={{alignItems:'center'}}>
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
                    <Button className={game.wiggleItems.includes(item) ? 'item-button anim' : 'item-button'} _active={{ bg:'#48454d', color:'white' }} onClick={() => game.toggleActive(item)} isActive={game.activeItems.includes(item)}>
                      {item}
                  </Button>
              ))}
              </HStack>
            </>
          ))}
          </Stack>

        <HStack align='baseline' style={{justifyContent:'center'}}>
          <Text> Mistakes:</Text> 
          {[...Array(3 - game.mistakes)].map(() =>
            <BsFillPersonFill color='grey'/>
          )}
          {[...Array(game.mistakes)].map(() =>
           <TbRectangleVerticalFilled color='red'/>
          )}

        </HStack>
        <HStack spacing={4} style={{justifyContent:'center'}}>
          <Button className='action-button' onClick={game.shuffle}>
            Shuffle
          </Button>
          <Button className='action-button' onClick={game.deselectAll}>
            Deselect All
          </Button>
          <Box as='button' className='chakra-button css-ez23ye action-button' disabled={game.activeItems.length < 4} onClick={game.submit}>
            Submit
          </Box>
        </HStack>
      </Stack>
      </Flex>
    </ChakraProvider>
    </>

  );
}

export default App;
