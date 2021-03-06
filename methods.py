# full list of methods from https://vk.com/dev/methods
methods = {
    'polls': (
        'getById',
        'addVote',
        'deleteVote',
        'getVoters',
        'create',
        'edit'
    ),
    'messages': (
        'get',
        'getDialogs',
        'getById',
        'search',
        'getHistory',
        'getHistoryAttachments',
        'send',
        'delete',
        'deleteDialog',
        'restore',
        'markAsRead',
        'markAsImportant',
        'getLongPollServer',
        'getLongPollHistory',
        'getChat',
        'createChat',
        'editChat',
        'getChatUsers',
        'setActivity',
        'searchDialogs',
        'addChatUser',
        'removeChatUser',
        'getLastActivity',
        'setChatPhoto',
        'deleteChatPhoto'
    ),
    'database': (
        'getCountries',
        'getRegions',
        'getStreetsById',
        'getCountriesById',
        'getCities',
        'getCitiesById',
        'getUniversities',
        'getSchools',
        'getSchoolClasses',
        'getFaculties',
        'getChairs'
    ),
    'account': (
        'getCounters',
        'setNameInMenu',
        'setOnline',
        'setOffline',
        'lookupContacts',
        'registerDevice',
        'unregisterDevice',
        'setSilenceMode',
        'getPushSettings',
        'setPushSettings',
        'getAppPermissions',
        'getActiveOffers',
        'banUser',
        'unbanUser',
        'getBanned',
        'getInfo',
        'setInfo',
        'changePassword',
        'getProfileInfo',
        'saveProfileInfo'
    ),
    'newsfeed': (
        'get',
        'getRecommended',
        'getComments',
        'getMentions',
        'getBanned',
        'addBan',
        'deleteBan',
        'ignoreItem',
        'unignoreItem',
        'search',
        'getLists',
        'saveList',
        'deleteList',
        'unsubscribe',
        'getSuggestedSources'
    ),
    'stats': (
        'get',
        'trackVisitor',
        'getPostReach'
    ),
    'likes': (
        'getList',
        'add',
        'delete',
        'isLiked'
    ),
    'widgets': (
        'getComments',
        'getPages'
    ),
    'auth': (
        'checkPhone',
        'signup',
        'confirm',
        'restore'
    ),
    'users': (
        'get',
        'search',
        'isAppUser',
        'getSubscriptions',
        'getFollowers',
        'report',
        'getNearby'
    ),
    'fave': (
        'getUsers',
        'getPhotos',
        'getPosts',
        'getVideos',
        'getLinks',
        'getMarketItems',
        'addUser',
        'removeUser',
        'addGroup',
        'removeGroup',
        'addLink',
        'removeLink'
    ),
    'gifts': (
        'get'
    ),
    'storage': (
        'get',
        'set',
        'getKeys'
    ),
    'photos': (
        'createAlbum',
        'editAlbum',
        'getAlbums',
        'get',
        'getAlbumsCount',
        'getById',
        'getUploadServer',
        'getOwnerPhotoUploadServer',
        'getChatUploadServer',
        'getMarketUploadServer',
        'getMarketAlbumUploadServer',
        'saveMarketPhoto',
        'saveMarketAlbumPhoto',
        'saveOwnerPhoto',
        'saveWallPhoto',
        'getWallUploadServer',
        'getMessagesUploadServer',
        'saveMessagesPhoto',
        'report',
        'reportComment',
        'search',
        'save',
        'copy',
        'edit',
        'move',
        'makeCover',
        'reorderAlbums',
        'reorderPhotos',
        'getAll',
        'getUserPhotos',
        'deleteAlbum',
        'delete',
        'restore',
        'confirmTag',
        'getComments',
        'getAllComments',
        'createComment',
        'deleteComment',
        'restoreComment',
        'editComment',
        'getTags',
        'putTag',
        'removeTag',
        'getNewTags'
    ),
    'utils': (
        'checkLink',
        'resolveScreenName',
        'getServerTime'
    ),
    'pages': (
        'get',
        'save',
        'saveAccess',
        'getHistory',
        'getTitles',
        'getVersion',
        'parseWiki',
        'clearCache'
    ),
    'friends': (
        'get',
        'getOnline',
        'getMutual',
        'getRecent',
        'getRequests',
        'add',
        'edit',
        'delete',
        'getLists',
        'addList',
        'editList',
        'deleteList',
        'getAppUsers',
        'getByPhones',
        'deleteAllRequests',
        'getSuggestions',
        'areFriends',
        'getAvailableForCall',
        'search'
    ),
    'wall': (
        'get',
        'search',
        'getById',
        'post',
        'repost',
        'getReposts',
        'edit',
        'delete',
        'restore',
        'pin',
        'unpin',
        'getComments',
        'addComment',
        'editComment',
        'deleteComment',
        'restoreComment',
        'reportPost',
        'reportComment'
    ),
    'groups': (
        'isMember',
        'getById',
        'get',
        'getMembers',
        'join',
        'leave',
        'search',
        'getCatalog',
        'getCatalogInfo',
        'getInvites',
        'getInvitedUsers',
        'banUser',
        'unbanUser',
        'getBanned',
        'create',
        'edit',
        'editPlace',
        'getSettings',
        'getRequests',
        'editManager',
        'invite',
        'addLink',
        'deleteLink',
        'editLink',
        'reorderLink',
        'removeUser',
        'approveRequest'
    ),
    'board': (
        'getTopics',
        'getComments',
        'addTopic',
        'addComment',
        'deleteTopic',
        'editTopic',
        'editComment',
        'restoreComment',
        'deleteComment',
        'openTopic',
        'closeTopic',
        'fixTopic',
        'unfixTopic'
    ),
    'audio': (
        'get',
        'getById',
        'getLyrics',
        'search',
        'getUploadServer',
        'save',
        'add',
        'delete',
        'edit',
        'reorder',
        'restore',
        'getAlbums',
        'addAlbum',
        'editAlbum',
        'deleteAlbum',
        'moveToAlbum',
        'setBroadcast',
        'getBroadcastList',
        'getRecommendations',
        'getPopular',
        'getCount'
    ),
    'apps': (
        'getCatalog',
        'get',
        'sendRequest',
        'deleteAppRequests',
        'getFriendsList',
        'getLeaderboard',
        'getScore'
    ),
    'search': (
        'getHints'
    ),
    'docs': (
        'get',
        'getById',
        'getUploadServer',
        'getWallUploadServer',
        'save',
        'delete',
        'add',
        'getTypes',
        'search',
        'edit'
    ),
    'places': (
        'add',
        'getById',
        'search',
        'checkin',
        'getCheckins',
        'getTypes'
    ),
    'market': (
        'get',
        'getById',
        'search',
        'getAlbums',
        'getAlbumById',
        'createComment',
        'getComments',
        'deleteComment',
        'restoreComment',
        'editComment',
        'reportComment',
        'getCategories',
        'report',
        'add',
        'edit',
        'delete',
        'restore',
        'reorderItems',
        'reorderAlbums',
        'addAlbum',
        'editAlbum',
        'deleteAlbum',
        'removeFromAlbum',
        'addToAlbum'
    ),
    'video': (
        'get',
        'edit',
        'add',
        'save',
        'delete',
        'restore',
        'search',
        'getUserVideos',
        'getAlbums',
        'getAlbumById',
        'addAlbum',
        'editAlbum',
        'deleteAlbum',
        'reorderAlbums',
        'reorderVideos',
        'addToAlbum',
        'removeFromAlbum',
        'getAlbumsByVideo',
        'getComments',
        'createComment',
        'deleteComment',
        'restoreComment',
        'editComment',
        'getTags',
        'putTag',
        'removeTag',
        'getNewTags',
        'report',
        'reportComment',
        'getCatalog',
        'getCatalogSection',
        'hideCatalogSection'
    ),
    'status': (
        'get',
        'set'
    ),
    'notes': (
        'get',
        'getById',
        'add',
        'edit',
        'delete',
        'getComments',
        'createComment',
        'editComment',
        'deleteComment',
        'restoreComment'
    ),
    'notifications': (
        'get',
        'markAsViewed'
    )
}
