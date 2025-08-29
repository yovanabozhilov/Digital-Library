const {
    ClassicEditor,
    Essentials,
    Paragraph,
    Heading,
    Bold,
    Italic,
    Underline,
    Font,
    FontColor,
    FontBackgroundColor,
    Alignment,
    List,
    Link,
    BlockQuote,
    HorizontalLine,
    Table,
    TableToolbar,
    TableProperties,
    TableCellProperties,
    Image,
    ImageUpload
} = CKEDITOR;

ClassicEditor
    .create(document.querySelector('#editor'), {
        licenseKey: 'eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3ODUxOTY3OTksImp0aSI6IjMyNjBjZmFmLTVmMjYtNDVkYy1iODM5LTAwNTYxMzA1YmIzMSIsImxpY2Vuc2VkSG9zdHMiOlsiMTI3LjAuMC4xIiwibG9jYWxob3N0IiwiMTkyLjE2OC4qLioiLCIxMC4qLiouKiIsIjE3Mi4qLiouKiIsIioudGVzdCIsIioubG9jYWxob3N0IiwiKi5sb2NhbCJdLCJ1c2FnZUVuZHBvaW50IjoiaHR0cHM6Ly9wcm94eS1ldmVudC5ja2VkaXRvci5jb20iLCJkaXN0cmlidXRpb25DaGFubmVsIjpbImNsb3VkIiwiZHJ1cGFsIl0sImxpY2Vuc2VUeXBlIjoiZGV2ZWxvcG1lbnQiLCJmZWF0dXJlcyI6WyJEUlVQIiwiRTJQIiwiRTJXIl0sInZjIjoiNWE3NjkzMjEifQ.t6g6Up2akpOWH2-TVZFpw2WlixNUIc7GZSW-v043u_XUwBjCVwEo5qRRVT-7tKp6-Eu3VKps9E4oyyH9NZ0I8w',
        simpleUpload: {
            uploadUrl: '/upload_image/',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        },
        plugins: [
            Essentials, Paragraph, Heading,
            Bold, Italic, Underline,
            Font, FontColor, FontBackgroundColor,
            Alignment, List, Link,
            BlockQuote, HorizontalLine,
            Table, TableToolbar, TableProperties, TableCellProperties,
            Image, ImageUpload
        ],
        toolbar: [
            'heading', '|',
            'bold', 'italic', 'underline', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
            'alignment', '|',
            'bulletedList', 'numberedList', '|',
            'insertTable', 'horizontalLine', '|',
            'imageUpload', 'blockQuote', 'link', '|',
            'undo', 'redo'
        ]
    })
    .then(editor => {
        window.editor = editor;
        document.querySelector('form').addEventListener('submit', function () {
            document.getElementById('hidden-content').value = editor.getData();
        });

        editor.model.document.on('change:data', () => {
            updateWordCount();
        });

        updateWordCount();
    })
    .catch(error => {
        console.error(error);
    });


function updateWordCount() {
    const text = editor.getData().replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
    const words = text ? text.split(' ').length : 0;
    document.getElementById('word-count').innerText = `Брой думи: ${words}`;
}
