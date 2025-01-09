let currentPath = '';
let pathHistory = [];
let currentFilePath = '';

function updateMetrics() {
    fetch('/metrics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('diskBar').style.width = data.disk + '%';
            document.getElementById('diskBar_t').textContent = "Utilisation du disque principal : " + data.disk + '%';
        });
}

function newtab() {
    window.open("/System/qr_code.png", '_blank');
}

function loadFiles(path = '') {
    fetch(`/files?path=${encodeURIComponent(path)}`)
        .then(response => response.json())
        .then(files => {
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = '';
            updateMetrics();
            if (editor.style.display === 'block') {
                editor.style.display = 'none';
            }
            files.forEach(file => {
                const li = document.createElement('li');
                li.className = 'file-item';
                li.onclick = () => {
                    if (file.isDirectory) {
                        openFolder(file.path);
                    } else {
                        openFile(file.path);
                    }
                };

                const icon = document.createElement('img');
                icon.src = file.isDirectory ? '/System/folder-pen.png' : '/System/file-pen.png';
                icon.className = 'file-icon';
                icon.onclick = () => {
                    if (file.isDirectory) {
                        openFolder(file.path);
                    } else {
                        openFile(file.path);
                    }
                };
                const name = document.createElement('span');
                name.className = 'file-name';
                name.textContent = file.name;
                name.onclick = () => {
                };

                const actions = document.createElement('div');
                actions.className = 'file-actions';

                const renameBtn = document.createElement('button');
                renameBtn.onclick = () => renameFile(file.path);

                const deleteBtn = document.createElement('button');
                deleteBtn.onclick = () => deleteFile(file.path, li);

                const downloadBtn = document.createElement('button');
                downloadBtn.onclick = () => downloadItem(file.path);

                const img = document.createElement('img');
                img.src = 'System/JSrename_icon.png'; // Remplacez par le chemin de votre image
                img.alt = 'Renommer'; // Texte alternatif pour l'accessibilité
                const img1 = document.createElement('img');
                img1.src = 'System/JSdelete_icon.png'; // Remplacez par le chemin de votre image
                img1.alt = 'Supprimer'; // Texte alternatif pour l'accessibilité
                const img2 = document.createElement('img');
                img2.src = 'System/JSdownload_icon.png'; // Remplacez par le chemin de votre image
                img2.alt = 'Télécharger'; // Texte alternatif pour l'accessibilité
                // Ajoutez l'image au bouton
                renameBtn.appendChild(img);
                deleteBtn.appendChild(img1);
                downloadBtn.appendChild(img2);

                actions.appendChild(renameBtn);
                actions.appendChild(deleteBtn);
                actions.appendChild(downloadBtn);

                li.appendChild(icon);
                li.appendChild(name);
                li.appendChild(actions);
                fileList.appendChild(li);
            });
        });
}

function openFolder(path) {
    if (currentPath !== path) {
        pathHistory.push(currentPath);
        currentPath = path;
        loadFiles(path);
    }
}

function openFile(path) {
    const editor = document.getElementById('editor');
    if (editor.style.display === 'block' && currentFilePath === path) {
        // Si l'éditeur est déjà ouvert et que le fichier actuel est le même, fermez l'éditeur
        editor.style.display = 'none';
    } else {
        // Sinon, ouvrez l'éditeur avec le contenu du fichier
        fetch(`/edit?path=${encodeURIComponent(path)}`)
            .then(response => response.text())
            .then(content => {
                currentFilePath = path;
                document.getElementById('file-content').value = content;
                editor.style.display = 'block';
            });
    }
}

function Stop() {
    var elements = document.getElementsByClassName('resource');
    if (elements.length > 0) {
        elements[0].style.display = 'none';
        var element = document.getElementsByClassName('stop');
        if (element.length > 0) {
            element[0].style.display = 'block';
        }

    } else {
        console.error("Erreur lors de l'arrêt. (2)");
    }
    fetch(`/stop`);
}

function saveFile() {
    const content = document.getElementById('file-content').value;
    fetch(`/save?path=${encodeURIComponent(currentFilePath)}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content })
    })
    .then(() => {
        document.getElementById('editor').style.display = 'none';
        loadFiles(currentPath);
    });
}

function createItem(type) {
    const name = prompt(`Nom du ${type}:`);
    if (name) {
        fetch(`/create?type=${type}&name=${encodeURIComponent(name)}&path=${encodeURIComponent(currentPath)}`, {
            method: 'POST'
        })
        .then(() => loadFiles(currentPath));
    }
}

function renameFile(path) {
    const newName = prompt('Nouveau nom:');
    if (newName) {
        fetch(`/rename?path=${encodeURIComponent(path)}&newName=${encodeURIComponent(newName)}`, {
            method: 'POST'
        })
        .then(() => loadFiles(currentPath));
    }
}

function deleteFile(path, element) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
        fetch(`/delete?path=${encodeURIComponent(path)}`, {
            method: 'DELETE'
        })
        .then(() => loadFiles(currentPath));
    }
}

function goBack() {
    if (pathHistory.length > 0) {
        currentPath = pathHistory.pop();
        loadFiles(currentPath);
    }
}

function downloadItem(path) {
    fetch(`/fileinfo?path=${encodeURIComponent(path)}`)
        .then(response => response.json())
        .then(info => {
            if (info.isDirectory) {
                fetch(`/download?path=${encodeURIComponent(path)}&type=directory`)
                    .then(response => response.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = `${path.split('/').pop()}.zip` || 'download.zip';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        loadFiles(currentPath)
                    })
                    .catch(error => console.error('Erreur lors du téléchargement du dossier:', error));
            } else {
                fetch(`/download?path=${encodeURIComponent(path)}&type=file`)
                    .then(response => response.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = path.split('/').pop() || 'download';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        loadFiles(currentPath)
                    })
                    .catch(error => console.error('Erreur lors du téléchargement du fichier:', error));
            }
        })
        .catch(error => console.error('Erreur lors de la vérification du chemin:', error));
}

function refresh() {
    currentPath = "";
    currentFilePath = "";
    loadFiles("");
}

function refileload() {
    const a = prompt("Chemin du Répertoire que vous souhaitez utiliser : ");
    loadFiles(a);
    currentFilePath = a;
    currentPath = a;
}

document.getElementById('search').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('#file-list li').forEach(li => {
        const fileName = li.querySelector('.file-name').textContent.toLowerCase();
        li.style.display = fileName.includes(searchTerm) ? '' : 'none';
    });
});

// Chargement initial
loadFiles('');
