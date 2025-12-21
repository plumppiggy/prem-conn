
import { Flex, Stack, Heading, HStack, Button } from '@chakra-ui/react';
import { Outlet, Link as RouterLink, useLocation } from 'react-router-dom';
import premLogo from '../fpl.png';


export default function Homepage() {
  const location = useLocation();

  return (
    <Flex>
      <Stack>
        <HStack>
          <Heading>Games</Heading>
          <img height='80px' width='60px' src={premLogo} />
        </HStack>

        <HStack>
          <Button as={RouterLink} to='/connections' colorScheme='pink'/>
        </HStack>

        <Outlet />
      </Stack>
    </Flex>
  )

}