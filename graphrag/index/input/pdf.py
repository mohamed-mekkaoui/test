# # Copyright (c) 2024 Microsoft Corporation.
# # Licensed under the MIT License

# """A module containing load method definition for PDF files."""

# import logging
# from io import BytesIO
# import pandas as pd
# import fitz
# from typing import Optional, Dict

# from graphrag.config.models.input_config import InputConfig
# from graphrag.index.input.util import load_files, process_data_columns
# from graphrag.storage.pipeline_storage import PipelineStorage

# logger = logging.getLogger(__name__)

# async def load_pdf(
#     config: InputConfig,
#     storage: PipelineStorage,
# ) -> pd.DataFrame:
#     """Load PDF inputs from a directory."""
#     logger.info("Loading PDF files from %s", config.storage.base_dir)

#     async def load_file(path: str, group: Optional[Dict] = None) -> pd.DataFrame:
#         if group is None:
#             group = {}
            
#         # Lire le fichier PDF
#         buffer = BytesIO(await storage.get(path, as_bytes=True))
#         doc = fitz.open(stream=buffer, filetype="pdf")
        
#         # Extraire le texte de toutes les pages
#         text_content = []
#         for page in doc:
#             text_content.append(page.get_text(sort=True))
        
#         # Créer un DataFrame avec le contenu du PDF
#         data = pd.DataFrame({
#             'content': [''.join(text_content)],  # Tout le texte en une seule ligne
#             'filename': [path],
#             'page_count': [len(doc)]
#         })

#         # Ajouter les métadonnées du groupe si présentes
#         additional_keys = group.keys()
#         if len(additional_keys) > 0:
#             data[[*additional_keys]] = data.apply(
#                 lambda _row: pd.Series([group[key] for key in additional_keys]), axis=1
#             )

#         # Traiter les colonnes de données selon la configuration
#         data = process_data_columns(data, config, path)

#         # Ajouter la date de création
#         creation_date = await storage.get_creation_date(path)
#         data["creation_date"] = data.apply(lambda _: creation_date, axis=1)

#         return data

#     return await load_files(load_file, config, storage)


import logging
from io import BytesIO
import pandas as pd
import fitz  # PyMuPDF

from graphrag.config.models.input_config import InputConfig
from graphrag.index.input.util import load_files, process_data_columns
from graphrag.storage.pipeline_storage import PipelineStorage

logger = logging.getLogger(__name__)

async def load_pdf(
    config: InputConfig,
    storage: PipelineStorage,
) -> pd.DataFrame:
    """Load PDF inputs from a directory."""
    logger.info("Loading PDF files from %s", config.storage.base_dir)

    async def load_file(path: str, group: dict | None = None) -> pd.DataFrame:
        if group is None:
            group = {}
            
        # Lire le fichier PDF
        buffer = BytesIO(await storage.get(path, as_bytes=True))
        doc = fitz.open(stream=buffer, filetype="pdf")
        
        # Extraire le texte de chaque page
        text_content = ""
        for page in doc:
            text_content += page.get_text(sort=True) + "\n"
            
        # Créer le DataFrame avec la colonne 'text' requise
        data = pd.DataFrame({
            'text': [text_content],  # Important : colonne 'text' requise
            'filename': [path],
            'total_pages': [len(doc)]
        })

        # Ajouter les métadonnées du groupe
        additional_keys = group.keys()
        if len(additional_keys) > 0:
            data[[*additional_keys]] = data.apply(
                lambda _row: pd.Series([group[key] for key in additional_keys]), axis=1
            )

        # Traiter les colonnes de données selon la configuration
        data = process_data_columns(data, config, path)

        # Ajouter la date de création
        creation_date = await storage.get_creation_date(path)
        data["creation_date"] = data.apply(lambda _: creation_date, axis=1)

        return data

    return await load_files(load_file, config, storage)