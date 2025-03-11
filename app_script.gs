function doGet(e) {
  var folderName = "LIVE"; // Folder where you store your .deb files
  var folder, files, latestFile, latestDate = 0, latestId = "";

  // Get all folders in your Drive
  var folders = DriveApp.getFoldersByName(folderName);
  if (!folders.hasNext()) {
    return ContentService.createTextOutput("Error: Folder not found.").setMimeType(ContentService.MimeType.TEXT);
  }
  folder = folders.next(); // Get the LIVE folder

  // Get all files in the LIVE folder
  files = folder.getFiles();
  while (files.hasNext()) {
    var file = files.next();
    var createdDate = file.getLastUpdated().getTime();
    if (createdDate > latestDate && file.getName().endsWith(".deb")) { // Only check .deb files
      latestDate = createdDate;
      latestFile = file;
      latestId = file.getId();
    }
  }

  if (latestId === "") {
    return ContentService.createTextOutput("Error: No .deb files found.").setMimeType(ContentService.MimeType.TEXT);
  }

  return ContentService.createTextOutput(latestId).setMimeType(ContentService.MimeType.TEXT);
}