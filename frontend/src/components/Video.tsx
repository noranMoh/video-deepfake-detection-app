import { ActionIcon, Badge, Button, Card, Group, Text, rem } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconCheck, IconTrash, IconX, IconZoomCheck } from '@tabler/icons-react';
import { useMutation } from 'react-query';
import { uploadVideo } from '../api';



function Video({ video, id, onDelete }: { video: File, id: string, onDelete: (name: string) => void }) {

    const xIcon = <IconX style={{ width: rem(20), height: rem(20) }} />;
    const checkIcon = <IconCheck style={{ width: rem(20), height: rem(20) }} />;

    const mutation = useMutation({
        mutationFn: (video: File) => {
            return uploadVideo(video)
        },
    })

    const onSubmit = () => {

        mutation.mutate(video, {
            onSuccess: (response) => {

                console.log('response', response)

                const prediction = response.data.prediction

                notifications.show({
                    title: prediction ? 'Bummer!' : 'All good!',
                    message: prediction ? `${video.name} is fake` : `${video.name} is real`,
                    autoClose: false,
                    position: 'top-center',
                    icon: prediction ? xIcon : checkIcon,
                    color: prediction ? 'red' : 'green'
                })
            }
        })


    }

    return (

        <Card withBorder shadow="sm" radius="md" mt="md" >
            <Card.Section withBorder inheritPadding py="xs">
                <Group align='center' justify="space-between">
                    <Group align='center'>
                        <Text fw={500}>{video?.name}</Text>
                        {mutation.data?.data ? mutation.data.data.prediction ? <Badge color='red'>Fake</Badge> : <Badge color='green'>Real</Badge> : null}
                    </Group>
                    <Group align='center'>
                        <Button onClick={() => onSubmit()} color="blue" loading={mutation.isLoading} loaderProps={{ type: 'dots' }} type='submit' variant="light" leftSection={<IconZoomCheck size={18} />} >Detect</Button>
                        <ActionIcon variant="light" color="red" aria-label="Settings" size='lg' onClick={() => onDelete(id)}>
                            <IconTrash style={{ width: '60%', height: '60%' }} stroke={1.5} />
                        </ActionIcon>
                    </Group>
                </Group>
            </Card.Section>
        </Card>

    )

}
export default Video
