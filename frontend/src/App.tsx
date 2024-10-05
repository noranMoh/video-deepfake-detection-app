import { Blockquote, Container, Title } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useState } from 'react';
import { DropZone } from './components/Dropzone';
import Video from './components/Video';

const getId = () => 'axxxx'.replace(/[x]/g, (value) => (Math.random() * 16 | 0).toString(16))

function App() {

  const [files, setFiles] = useState<{file: File, id: string}[]>([])

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setFiles((currentFiles) => [...currentFiles, {file, id: getId()}])
    }
  };

  const onDelete = (id: string) => {
    setFiles((currentFiles) => currentFiles.filter(file => file.id !== id))
  }

  return (
    <Container mt="md" mb='md'>
      <Title order={1}>Deepfake Detection Tool</Title>

      <Blockquote color="blue" icon={<IconInfoCircle />} mt="xl">
        This tool uses an advanced ensemble of four detection models to identify fake videos.
        Two models focus on spatial features, analyzing patterns in individual frames, while the other two examine temporal features,
        tracking motion between frames using optical flow. By combining these approaches,
        the tool offers a more reliable way to detect video manipulation.
      </Blockquote>

      <DropZone mt="md" onDrop={onDrop} />

      {files.map(item => (
        <Video key={item.id} video={item.file} id={item.id} onDelete={onDelete} />
      ))}

    </Container>

  )

}
export default App
