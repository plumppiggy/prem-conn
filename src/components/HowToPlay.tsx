import {Modal, ModalContent, ModalHeader, ModalOverlay, useDisclosure, ModalCloseButton, ModalBody, IconButton, ModalFooter} from '@chakra-ui/react'
import { BsQuestionCircle } from 'react-icons/bs';
function HowToPlay() {
  const {isOpen, onOpen, onClose} = useDisclosure();
  return (
    <>
    <IconButton aria-label='How to Play' onClick={onOpen} icon={<BsQuestionCircle/>}></IconButton>
    
    <Modal isOpen={isOpen} onClose={onClose} isCentered size="lg">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>How to Play Premier League Connections</ModalHeader>
        <ModalCloseButton />
        <ModalBody fontSize='sm'>
            <h3 style={{fontSize: '1rem'}}>Find groups of four premier league players which played for the same team.</h3>
            <div className='how-to-play-list'>
              <ul>
                <li>
                  Select four players and press 'Submit' to check if your guess is correct.
                </li>
                <li>
                  Find all the groups without making three mistakes.
                </li>
              </ul>
            </div>
            
            The categories will always be Premier League teams! <br/>
            Each puzzle has exactly one solution, but some players may have played together in different teams!
        </ModalBody>
        <ModalFooter fontSize='xs'>
          Made by Elysia Darbourne
        </ModalFooter>
      </ModalContent>
    </Modal>
    </>
  )
}

export default HowToPlay;