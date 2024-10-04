import { Badge, Blockquote, Button, Card, Container, Group, Text, Title, rem } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconCheck, IconInfoCircle, IconX, IconZoomCheck } from '@tabler/icons-react';
import { useState } from 'react';
import { useMutation } from 'react-query';
import { uploadVideo } from './api';
import { DropZone } from './components/dropzone';



function App() {

  const xIcon = <IconX style={{ width: rem(20), height: rem(20) }} />;
  const checkIcon = <IconCheck style={{ width: rem(20), height: rem(20) }} />;


  const mutation = useMutation({
    mutationFn: (video: File) => {
      return uploadVideo(video)
    },
  })

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    mutation.reset()
    if (file) {
      setSelectedFile(file);
    }
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {

    e.preventDefault();
    if (!selectedFile) {
      console.error("No file selected.");
      return;
    }

    mutation.mutate(selectedFile, {
      onSuccess: (response) => {

        const prediction = response.data.prediction

        notifications.show({
          title: prediction ? 'Bummer!' : 'All good!',
          message: prediction ? 'Video is fake' : 'Video is real',
          autoClose: false,
          position: 'top-center',
          icon: prediction ? xIcon : checkIcon,
          color: prediction ? 'red' : 'green'
        })
      }
    })


  }

  return (
    <Container mt="md">
      <Title order={1}>Deepfake Detection Tool</Title>

      <Blockquote color="blue" icon={<IconInfoCircle />} mt="xl">
        This tool uses an advanced ensemble of four detection models to identify fake videos.
        Two models focus on spatial features, analyzing patterns in individual frames, while the other two examine temporal features,
        tracking motion between frames using optical flow. By combining these approaches,
        the tool offers a more reliable way to detect video manipulation.
      </Blockquote>

      <form onSubmit={onSubmit} encType="multipart/form-data" >
        <DropZone mt="md" onDrop={onDrop} />
        {selectedFile ? <Card withBorder shadow="sm" radius="md" mt="md" >
          <Card.Section withBorder inheritPadding py="xs">
            <Group align='center' justify="space-between">
              <Group align='center'>
                <Text fw={500}>{selectedFile?.name}</Text>
                {mutation.data?.data ? mutation.data?.data?.prediction ? <Badge color='red'>Fake</Badge> : <Badge color='green'>Real</Badge> : null}
              </Group>
              <Button color="blue" loading={mutation.isLoading} loaderProps={{ type: 'dots' }} type='submit' variant="light" leftSection={<IconZoomCheck size={18} />} >Detect</Button>
            </Group>
          </Card.Section>
        </Card> : null}
      </form>

    </Container>

  )

}
export default App
