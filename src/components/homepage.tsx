
import { Flex, Stack, Heading, HStack, Button, Center } from '@chakra-ui/react';
import { Outlet, Link as RouterLink, useLocation } from 'react-router-dom';
import premLogo from '../fpl.png';


export default function Homepage() {
  const location = useLocation();

  const currPage = location.pathname.includes('/connections')

  return (
    <Flex h='100%' w='100%' align='center' justify='center' style={{padding: '1vh'}}>
      <Stack spacing={4} w='100%' maxW='800px'>
        <HStack>
          <Heading>Elysia's Collection of Web Games</Heading>
          <img height='80px' width='60px' src={premLogo} />
        </HStack>

        <HStack>
          <Button as={RouterLink} to='/connections' 
            colorScheme={currPage ? 'pink' : 'gray'} variant={currPage ? 'solid': 'outline'}>
            Connections
          </Button>
          <Button as={RouterLink} to='/crossword' 
            colorScheme={!currPage ? 'pink' : 'gray'} variant={!currPage ? 'solid': 'outline'}>
            Crossword
          </Button>
        </HStack>

        <Outlet />
      </Stack>
    </Flex>
  )

}