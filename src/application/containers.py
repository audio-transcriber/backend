from dependency_injector import containers, providers

from application.transcription.usecases import TranscriptionUseCase


class TranscriptionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['presentation.http.transcription.route'])

    sio_container = providers.DependenciesContainer()
    bytes_storage_container = providers.DependenciesContainer()
    message_broker_container = providers.DependenciesContainer()

    usecase = providers.Factory(
        TranscriptionUseCase,
        sio_container.sio,
        providers.Factory(bytes_storage_container.adapter),
        providers.Factory(message_broker_container.producer),
    )
