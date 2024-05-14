package kvstore

import (
	"bytes"
	"crypto/ecdsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"github.com/google/uuid"
	"github.com/tendermint/tendermint/abci/example/code"
	"github.com/tendermint/tendermint/abci/types"
	"github.com/tendermint/tendermint/version"
	dbm "github.com/tendermint/tm-db"
	"net/http"
)

var (
	stateKey        = []byte("stateKey")
	kvPairPrefixKey = []byte("kvPairKey:")

	ProtocolVersion uint64 = 0x1
)

type State struct {
	db      dbm.DB
	Size    int64  `json:"size"`
	Height  int64  `json:"height"`
	AppHash []byte `json:"app_hash"`
}

func loadState(db dbm.DB) State {
	var state State
	state.db = db
	stateBytes, err := db.Get(stateKey)
	if err != nil {
		panic(err)
	}
	if len(stateBytes) == 0 {
		return state
	}
	err = json.Unmarshal(stateBytes, &state)
	if err != nil {
		panic(err)
	}
	return state
}

func saveState(state State) {
	stateBytes, err := json.Marshal(state)
	if err != nil {
		panic(err)
	}
	err = state.db.Set(stateKey, stateBytes)
	if err != nil {
		panic(err)
	}
}

func prefixKey(key []byte) []byte {
	return append(kvPairPrefixKey, key...)
}

//---------------------------------------------------

var _ types.Application = (*Application)(nil)

type Application struct {
	types.BaseApplication

	state        State
	RetainBlocks int64 // blocks to retain after commit (via ResponseCommit.RetainHeight)
}

type User struct {
	PublicKey string `json:"public_key"`
	Amount    int64  `json:"amount"`
	ShareList string `json:"sharelist"`
}
type QueryData struct {
	PublicKey string `json:"public_key"`
	DataStr   string `json:"dataStr"`
	Signature string `json:"signature"`
}
type ShareData struct {
	PublicKey     string `json:"public_key"`
	DataStr       string `json:"dataStr"`
	Signature     string `json:"signature"`
	Data          string `json:"data"`
	PermissionCtr string `json:"permissionCtr"`
	WhoGet        string `json:"whoGet"`
	WhoObey       string `json:"whoObey"`
}
type DownLoadData struct {
	PublicKey string `json:"public_key"`
	DataStr   string `json:"dataStr"`
	Signature string `json:"signature"`
	DataKey   string `json:"data"`
}
type PermissionContract struct {
	Permissions map[string][]string
}

// 分享数据，除了验证身份以外，需要有权限列表

func NewApplication() *Application {
	state := loadState(dbm.NewMemDB())

	//
	application := &Application{state: state}

	http.Handle("/", application)
	fmt.Println("Listening on port 8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		return nil
	}
	return &Application{state: state}
}

func (app *Application) Info(req types.RequestInfo) (resInfo types.ResponseInfo) {
	return types.ResponseInfo{
		Data:             fmt.Sprintf("{\"size\":%v}", app.state.Size),
		Version:          version.ABCIVersion,
		AppVersion:       ProtocolVersion,
		LastBlockHeight:  app.state.Height,
		LastBlockAppHash: app.state.AppHash,
	}
}

// tx is either "key=value" or just arbitrary bytes
func (app *Application) DeliverTx(req types.RequestDeliverTx) types.ResponseDeliverTx {
	var key, value []byte
	parts := bytes.Split(req.Tx, []byte("="))
	if len(parts) == 2 {
		key, value = parts[0], parts[1]
	} else {
		key, value = req.Tx, req.Tx
	}

	err := app.state.db.Set(prefixKey(key), value)
	if err != nil {
		panic(err)
	}
	app.state.Size++

	events := []types.Event{
		{
			Type: "app",
			Attributes: []types.EventAttribute{
				{Key: []byte("creator"), Value: []byte("Cosmoshi Netowoko"), Index: true},
				{Key: []byte("key"), Value: key, Index: true},
				{Key: []byte("index_key"), Value: []byte("index is working"), Index: true},
				{Key: []byte("noindex_key"), Value: []byte("index is working"), Index: false},
			},
		},
	}

	return types.ResponseDeliverTx{Code: code.CodeTypeOK, Events: events}
}

func (app *Application) CheckTx(req types.RequestCheckTx) types.ResponseCheckTx {
	return types.ResponseCheckTx{Code: code.CodeTypeOK, GasWanted: 1}
}

func (app *Application) Commit() types.ResponseCommit {
	// Using a memdb - just return the big endian size of the db
	appHash := make([]byte, 8)
	binary.PutVarint(appHash, app.state.Size)
	app.state.AppHash = appHash
	app.state.Height++
	saveState(app.state)

	resp := types.ResponseCommit{Data: appHash}
	if app.RetainBlocks > 0 && app.state.Height >= app.RetainBlocks {
		resp.RetainHeight = app.state.Height - app.RetainBlocks + 1
	}
	return resp
}

// Returns an associated value or nil if missing.
func (app *Application) Query(reqQuery types.RequestQuery) (resQuery types.ResponseQuery) {
	if reqQuery.Prove {
		value, err := app.state.db.Get(prefixKey(reqQuery.Data))
		if err != nil {
			panic(err)
		}
		if value == nil {
			resQuery.Log = "does not exist"
		} else {
			resQuery.Log = "exists"
		}
		resQuery.Index = -1 // TODO make Proof return index
		resQuery.Key = reqQuery.Data
		resQuery.Value = value
		resQuery.Height = app.state.Height

		return
	}

	resQuery.Key = reqQuery.Data
	value, err := app.state.db.Get(prefixKey(reqQuery.Data))
	if err != nil {
		panic(err)
	}
	if value == nil {
		resQuery.Log = "does not exist"
	} else {
		resQuery.Log = "exists"
	}
	resQuery.Value = value
	resQuery.Height = app.state.Height

	return resQuery
}

func (app *Application) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		app.handleGet(w, r)
	case "POST":
		app.handlePost(w, r)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
func (app *Application) handlePost(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/query":
		app.handleQueryRequest(w, r)
	case "/share":
		app.handleShareRequest(w, r)
	case "/download":
		app.handleDownloadRequest(w, r)
	case "/obey":
		app.handleObeyRequest(w, r)
	default:
		http.Error(w, "Invalid URL", http.StatusNotFound)
	}
}

func (app *Application) handleQueryRequest(w http.ResponseWriter, r *http.Request) {
	var requestData QueryData
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	queryResponse := app.handleQuery(requestData)

	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(struct{ QueryResponse types.ResponseQuery }{QueryResponse: queryResponse})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (app *Application) handleShareRequest(w http.ResponseWriter, r *http.Request) {
	var requestData ShareData
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	shareResponse := app.handleShare(requestData)

	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(struct{ ShareResponse types.ResponseQuery }{ShareResponse: shareResponse})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (app *Application) handleDownloadRequest(w http.ResponseWriter, r *http.Request) {
	var requestData DownLoadData
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	downloadResponse := app.handleLoad(requestData)

	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(struct{ LoadResponse types.ResponseQuery }{LoadResponse: downloadResponse})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
func (app *Application) handleObeyRequest(w http.ResponseWriter, r *http.Request) {
	var requestData DownLoadData
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	downloadResponse := app.handleObey(requestData)

	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(struct{ LoadResponse types.ResponseQuery }{LoadResponse: downloadResponse})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (app *Application) handleGet(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	if key == "" {
		http.Error(w, "Missing key parameter", http.StatusBadRequest)
		return
	}

	reqQuery := types.RequestQuery{Data: []byte(key)}
	response := app.Query(reqQuery)

	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(response)
	if err != nil {
		return
	}
}

//	func (app *Application) handleQuery(query string) types.ResponseQuery {
//		// 解析查询参数，这里假设查询参数是键名
//		key := []byte(query)
//
//		// 从 kvstore 中获取存储的值
//		value, err := app.state.db.Get(key)
//		if err != nil {
//			// 如果发生错误，返回查询失败的响应
//			return types.ResponseQuery{
//				Log:    err.Error(),
//				Height: app.state.Height,
//			}
//		}
//
//		// 构造查询成功的响应，包含键名、值和当前高度信息
//		return types.ResponseQuery{
//			Key:    key,
//			Value:  value,
//			Log:    "exists",
//			Height: app.state.Height,
//		}
//	}

func (app *Application) handleQuery(requestData QueryData) types.ResponseQuery {
	// 获取键名
	PublicKey := []byte(requestData.PublicKey)
	Signature := []byte(requestData.Signature)
	Data := []byte(requestData.DataStr)
	_, err := app.state.db.Get(PublicKey)
	hash := sha256.Sum256(Data)
	originalPublicKey := string(PublicKey)
	// 调试语句
	fmt.Println("Query:", requestData)
	fmt.Println("Public Key Length:", len(requestData.PublicKey))
	fmt.Printf("Public Key Hex: %x\n", PublicKey)
	fmt.Println("Signature Length:", len(requestData.Signature))
	fmt.Printf("Signature Hex: %x\n", Signature)
	fmt.Println("Data Length:", len(requestData.DataStr))
	fmt.Printf("Data Hex: %x\n", Data)
	fmt.Printf("Public Key: %s\n", string(PublicKey))
	fmt.Printf("originalPublicKey: %s\n", originalPublicKey)
	fmt.Printf("Signature: %s\n", string(Signature))
	fmt.Printf("Data: %s\n", string(Data))
	fmt.Printf("Data Hash: %x\n", hash)
	fmt.Println("Hash:", hex.EncodeToString(hash[:]))
	block, _ := pem.Decode(PublicKey)
	if block == nil {
		// 处理错误，无法解码公钥字符串
		return types.ResponseQuery{
			Log:    "身份验证失败，无法解码公钥字符串",
			Height: app.state.Height,
		}
	}
	// 解析公钥
	pubKey, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		// 处理错误，无法解析公钥
		return types.ResponseQuery{
			Log:    err.Error() + "111",
			Height: app.state.Height,
		}
	}
	ecdsaPubKey, ok := pubKey.(*ecdsa.PublicKey)
	if !ok {
		// 处理错误，公钥类型不是 ECDSA
		return types.ResponseQuery{
			Log:    "公钥类型不是 ECDSA",
			Height: app.state.Height,
		}
	}
	fmt.Println("Public key parsed successfully:", ecdsaPubKey)
	// 验证签名
	valid := ecdsa.VerifyASN1(ecdsaPubKey, hash[:], Signature)
	if valid {
		// 签名有效，可以继续处理交易或其他操作
		fmt.Println("Signature is valid")
		// 从 kvstore 中获取存储的值
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}

		// 构造查询成功的响应，包含键名、值和当前高度信息
		return types.ResponseQuery{
			//Key:    PublicKey,
			Value:  value,
			Log:    "签名有效，exists",
			Height: app.state.Height,
		}
	} else {
		// 签名无效，可能是伪造的交易或者其他错误
		fmt.Println("Signature is invalid")
		//return types.ResponseQuery{
		//	Log:    "Signature is invalid",
		//	Height: app.state.Height,
		//}
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}
		if value == nil {
			app.CreateUserAndSubmitToBlockchain(requestData.PublicKey)
			user, err := app.QueryUser(requestData.PublicKey)
			userJSON, err := json.Marshal(user)
			if err != nil {
				// 处理查询错误
				fmt.Println("Error querying user:", err)
			} else {
				// 打印用户信息
				fmt.Println("User PublicKey:", user.PublicKey)
				fmt.Println("User Amount:", user.Amount)
				fmt.Println("User ShareList:", user.ShareList)
			}
			return types.ResponseQuery{
				//Key:    []byte(requestData.PublicKey),
				Value:  userJSON,
				Log:    "新用户，区块链已自动注册",
				Height: app.state.Height,
			}
		}
		// 构造查询成功的响应，包含键名、值和当前高度信息
		user, err := app.QueryUser(requestData.PublicKey)
		userJSON, err := json.Marshal(user)
		if err != nil {
			// 处理查询错误
			fmt.Println("Error querying user:", err)
		} else {
			// 打印用户信息
			fmt.Println("User PublicKey:", user.PublicKey)
			fmt.Println("User Amount:", user.Amount)
			fmt.Println("User ShareList:", user.ShareList)
		}
		return types.ResponseQuery{
			//Key:    []byte(requestData.PublicKey),
			Value:  userJSON,
			Log:    "查询用户信息成功",
			Height: app.state.Height,
		}
	}
	// 验证通过，以下是处理data
}
func (app *Application) handleShare(requestData ShareData) types.ResponseQuery {
	// 获取键名
	PublicKey := []byte(requestData.PublicKey)
	Signature := []byte(requestData.Signature)
	DataStr := []byte(requestData.DataStr)
	hash := sha256.Sum256(DataStr)
	block, _ := pem.Decode([]byte(PublicKey))
	if block == nil {
		// 处理错误，无法解码公钥字符串
		return types.ResponseQuery{
			Log:    "身份验证失败，无法解码公钥字符串",
			Height: app.state.Height,
		}
	}
	// 解析公钥
	pubKey, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		// 处理错误，无法解析公钥
		return types.ResponseQuery{
			Log:    err.Error(),
			Height: app.state.Height,
		}
	}
	ecdsaPubKey, ok := pubKey.(*ecdsa.PublicKey)
	if !ok {
		// 处理错误，公钥类型不是 ECDSA
		return types.ResponseQuery{
			Log:    "公钥类型不是 ECDSA",
			Height: app.state.Height,
		}
	}

	valid := ecdsa.VerifyASN1(ecdsaPubKey, hash[:], Signature)
	if valid {
		// 签名有效，可以继续处理交易或其他操作
		fmt.Println("Signature is valid")
		// 从 kvstore 中获取存储的值
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}

		// 构造查询成功的响应，包含键名、值和当前高度信息
		return types.ResponseQuery{
			//Key:    PublicKey,
			Value:  value,
			Log:    "签名有效，exists",
			Height: app.state.Height,
		}
	} else {
		fmt.Println("Signature is invalid")
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}
		// 构造查询成功的响应，包含键名、值和当前高度信息
		user, err := app.QueryUser(requestData.PublicKey)
		//userJSON, err := json.Marshal(user)
		if err != nil {
			// 处理查询错误
			fmt.Println("Error querying user:", err)
			return types.ResponseQuery{
				Log:    "数据上传失败：用户未注册",
				Height: app.state.Height,
			}
		} else {
			// 打印用户信息
			fmt.Println("User PublicKey:", user.PublicKey)
			fmt.Println("User Amount:", user.Amount)
			fmt.Println("User ShareList:", user.ShareList)
		}
		// 上传数据
		app.DataShare(requestData)
		value, err = app.state.db.Get(PublicKey)
		return types.ResponseQuery{
			//Key:    []byte(requestData.PublicKey),
			Value:  value,
			Log:    "数据上传成功",
			Height: app.state.Height,
		}
	}
}
func (app *Application) handleLoad(requestData DownLoadData) types.ResponseQuery {
	// 获取键名
	PublicKey := []byte(requestData.PublicKey)
	Signature := []byte(requestData.Signature)
	DataStr := []byte(requestData.DataStr)
	DataKey := []byte(requestData.DataKey)
	hash := sha256.Sum256(DataStr)
	block, _ := pem.Decode([]byte(PublicKey))
	if block == nil {
		// 处理错误，无法解码公钥字符串
		return types.ResponseQuery{
			Log:    "身份验证失败，无法解码公钥字符串",
			Height: app.state.Height,
		}
	}
	// 解析公钥
	pubKey, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		// 处理错误，无法解析公钥
		return types.ResponseQuery{
			Log:    err.Error(),
			Height: app.state.Height,
		}
	}
	ecdsaPubKey, ok := pubKey.(*ecdsa.PublicKey)
	if !ok {
		// 处理错误，公钥类型不是 ECDSA
		return types.ResponseQuery{
			Log:    "公钥类型不是 ECDSA",
			Height: app.state.Height,
		}
	}

	// 验证签名
	valid := ecdsa.VerifyASN1(ecdsaPubKey, hash[:], Signature)
	if valid {
		// 签名有效，可以继续处理交易或其他操作
		fmt.Println("Signature is valid")
		// 从 kvstore 中获取存储的值
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}

		// 构造查询成功的响应，包含键名、值和当前高度信息
		return types.ResponseQuery{
			//Key:    PublicKey,
			Value:  value,
			Log:    "exists",
			Height: app.state.Height,
		}
	} else {
		// 签名无效，可能是伪造的交易或者其他错误
		fmt.Println("Signature is invalid")
		// 构造查询成功的响应，包含键名、值和当前高度信息
		user, err := app.QueryUser(requestData.PublicKey)
		//userJSON, err := json.Marshal(user)
		if err != nil {
			// 处理查询错误
			fmt.Println("Error querying user:", err)
			return types.ResponseQuery{
				Log:    "数据下载失败：用户未注册",
				Height: app.state.Height,
			}
		} else {
			// 打印用户信息
			fmt.Println("User PublicKey:", user.PublicKey)
			fmt.Println("User Amount:", user.Amount)
			fmt.Println("User ShareList:", user.ShareList)
		}
		// 获取数据
		Data, flag := app.GetDataByID(string(DataKey), string(PublicKey))
		DataJSON, err := json.Marshal(Data)
		if flag != 1 {
			return types.ResponseQuery{
				//Key:    []byte(requestData.PublicKey),
				Value:  DataJSON,
				Log:    "数据下载失败",
				Height: app.state.Height,
			}
		}
		return types.ResponseQuery{
			//Key:    []byte(requestData.PublicKey),
			Value:  DataJSON,
			Log:    "数据下载成功",
			Height: app.state.Height,
		}
	}
}
func (app *Application) handleObey(requestData DownLoadData) types.ResponseQuery {
	// 获取键名
	PublicKey := []byte(requestData.PublicKey)
	Signature := []byte(requestData.Signature)
	DataStr := []byte(requestData.DataStr)
	DataKey := []byte(requestData.DataKey)
	hash := sha256.Sum256(DataStr)
	block, _ := pem.Decode([]byte(PublicKey))
	if block == nil {
		// 处理错误，无法解码公钥字符串
		return types.ResponseQuery{
			Log:    "身份验证失败，无法解码公钥字符串",
			Height: app.state.Height,
		}
	}
	// 解析公钥
	pubKey, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		// 处理错误，无法解析公钥
		return types.ResponseQuery{
			Log:    err.Error(),
			Height: app.state.Height,
		}
	}
	ecdsaPubKey, ok := pubKey.(*ecdsa.PublicKey)
	if !ok {
		// 处理错误，公钥类型不是 ECDSA
		return types.ResponseQuery{
			Log:    "公钥类型不是 ECDSA",
			Height: app.state.Height,
		}
	}

	// 验证签名
	valid := ecdsa.VerifyASN1(ecdsaPubKey, hash[:], Signature)
	if valid {
		// 签名有效，可以继续处理交易或其他操作
		fmt.Println("Signature is valid")
		// 从 kvstore 中获取存储的值
		value, err := app.state.db.Get(PublicKey)
		if err != nil {
			// 如果发生错误，返回查询失败的响应
			return types.ResponseQuery{
				Log:    err.Error(),
				Height: app.state.Height,
			}
		}

		// 构造查询成功的响应，包含键名、值和当前高度信息
		return types.ResponseQuery{
			//Key:    PublicKey,
			Value:  value,
			Log:    "exists",
			Height: app.state.Height,
		}
	} else {
		// 签名无效，可能是伪造的交易或者其他错误
		fmt.Println("Signature is invalid")
		// 构造查询成功的响应，包含键名、值和当前高度信息
		user, err := app.QueryUser(requestData.PublicKey)
		//userJSON, err := json.Marshal(user)
		if err != nil {
			// 处理查询错误
			fmt.Println("Error querying user:", err)
			return types.ResponseQuery{
				Log:    "数据违约失败：用户未注册",
				Height: app.state.Height,
			}
		} else {
			// 打印用户信息
			fmt.Println("User PublicKey:", user.PublicKey)
			fmt.Println("User Amount:", user.Amount)
			fmt.Println("User ShareList:", user.ShareList)
		}
		// 获取数据
		Data, flag := app.ObeyDataByID(string(DataKey), string(PublicKey))
		DataJSON, err := json.Marshal(Data)
		if flag != 1 {
			return types.ResponseQuery{
				//Key:    []byte(requestData.PublicKey),
				Value:  DataJSON,
				Log:    "数据违约失败",
				Height: app.state.Height,
			}
		}
		return types.ResponseQuery{
			//Key:    []byte(requestData.PublicKey),
			Value:  DataJSON,
			Log:    "数据违约成功",
			Height: app.state.Height,
		}
	}
}

func parseJSONQuery(jsonQuery string) (QueryData, error) {
	var queryData QueryData

	// 解析 JSON 字符串为 QueryData 结构体
	if err := json.Unmarshal([]byte(jsonQuery), &queryData); err != nil {
		return QueryData{}, err
	}

	return queryData, nil
}

// 权限控制

func NewPermissionContract() *PermissionContract {
	return &PermissionContract{
		Permissions: make(map[string][]string),
	}
}

func (pc *PermissionContract) GrantPermission(user string, permissions []string) {
	pc.Permissions[user] = permissions
}

func (pc *PermissionContract) RevokePermission(user string) {
	delete(pc.Permissions, user)
}

func (pc *PermissionContract) CheckPermission(user string, action string) bool {
	allowedPermissions, ok := pc.Permissions[user]
	if !ok {
		return false // 用户不存在或未授予任何权限
	}

	for _, p := range allowedPermissions {
		if p == action {
			return true // 用户被授权执行该操作
		}
	}

	return false // 用户未被授权执行该操作
}

// 创建用户
func (app *Application) CreateUserAndSubmitToBlockchain(publicKey string) types.ResponseDeliverTx {
	// 创建一个新的 User 结构体
	user := User{
		PublicKey: publicKey,
		Amount:    10,
		ShareList: "shareRecords:", // 将 shareList 初始化为空字符串
	}

	// 将 User 结构体编码为 JSON 格式
	userJSON, err := json.Marshal(user)
	if err != nil {
		panic(err)
	}

	// 提交到区块链
	err = app.state.db.Set([]byte(publicKey), userJSON)
	if err != nil {
		panic(err)
	}

	// 构造事件
	events := []types.Event{
		{
			Type: "user_creation",
			Attributes: []types.EventAttribute{
				{Key: []byte("creator"), Value: []byte("YourAppName"), Index: true},
				{Key: []byte("public_key"), Value: []byte(publicKey), Index: true},
			},
		},
	}

	// 返回响应
	return types.ResponseDeliverTx{Code: code.CodeTypeOK, Events: events}
}
func (app *Application) QueryUser(publicKey string) (User, error) {
	// 从区块链中检索用户信息
	userJSON, err := app.state.db.Get([]byte(publicKey))
	if err != nil {
		return User{}, err
	}

	// 解码 JSON 数据为 User 结构体
	var user User
	err = json.Unmarshal(userJSON, &user)
	if err != nil {
		return User{}, err
	}

	return user, nil
}

// 创建共享数据交易
func (app *Application) DataShare(data ShareData) types.ResponseDeliverTx {
	// 解析交易
	id := uuid.New()
	// 将 UUID 转换为字符串
	uu_id := id.String()
	fmt.Println("uu_id:", uu_id)
	// 存储数据到区块链
	dataBytes, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	err = app.state.db.Set([]byte(uu_id), dataBytes)
	if err != nil {
		panic(err)
	}
	user, err := app.QueryUser(data.PublicKey)
	if user != (User{}) {
		// 如果user是空结构体User{}
		tmpstr := user.ShareList
		user.ShareList = tmpstr + uu_id + ";"
		userJSON, err := json.Marshal(user)
		if err != nil {
			panic(err)
		}
		// 提交到区块链
		err = app.state.db.Set([]byte(data.PublicKey), userJSON)

	}
	err = app.state.db.Set([]byte(uu_id), dataBytes)
	return types.ResponseDeliverTx{
		Code: types.CodeTypeOK,
		Log:  "Transaction successfully processed",
	}
}

func (app *Application) GetDataByID(id string, ckey string) (ShareData, int) {
	dataJSON, err := app.state.db.Get([]byte(id))
	if err != nil {
		return ShareData{}, 0
	}

	// 解码 JSON 数据为 ShareData 结构体
	var data ShareData
	err = json.Unmarshal(dataJSON, &data)
	if err != nil {
		return ShareData{}, 0
	}
	permissionCtr := []byte(data.PermissionCtr)
	owner := []byte(data.PublicKey)
	fmt.Println("这是获取到的Share数据的可读权限key：", string(permissionCtr))
	fmt.Println("这是下载者的key：", ckey)
	if string(permissionCtr) == ckey {
		tmpstr := data.WhoGet
		data.WhoGet = tmpstr + ckey + ";"
		dataBytes, err := json.Marshal(data)
		if err != nil {
			panic(err)
		}
		err = app.state.db.Set([]byte(id), dataBytes)
		return data, 1
	}
	if ckey == string(owner) {
		return data, 1
	}
	return ShareData{}, 0
}
func (app *Application) ObeyDataByID(id string, ckey string) (ShareData, int) {
	dataJSON, err := app.state.db.Get([]byte(id))
	if err != nil {
		return ShareData{}, 0
	}

	// 解码 JSON 数据为 ShareData 结构体
	var data ShareData
	err = json.Unmarshal(dataJSON, &data)
	if err != nil {
		return ShareData{}, 0
	}
	permissionCtr := []byte(data.PermissionCtr)
	owner := []byte(data.PublicKey)
	fmt.Println("这是获取到的Share数据的可读权限key：", string(permissionCtr))
	fmt.Println("这是下载者的key：", ckey)
	if string(permissionCtr) == ckey {
		tmpstr := data.WhoObey
		data.WhoObey = tmpstr + ckey + ";"
		dataBytes, err := json.Marshal(data)
		if err != nil {
			panic(err)
		}
		err = app.state.db.Set([]byte(id), dataBytes)
		app.payAmount(ckey, string(owner))
		return data, 1
	}
	return ShareData{}, 0
}
func (app *Application) payAmount(A_key string, B_key string) (User, int) {
	user1, err := app.QueryUser(A_key)
	if err != nil {
		panic(err)
	}
	user2, err := app.QueryUser(B_key)
	if err != nil {
		panic(err)
	}
	user1.Amount -= 1
	user2.Amount += 1
	userJSON1, err := json.Marshal(user1)
	if err != nil {
		panic(err)
	}
	userJSON2, err := json.Marshal(user2)
	if err != nil {
		panic(err)
	}
	// 提交到区块链
	err = app.state.db.Set([]byte(user1.PublicKey), userJSON1)
	err = app.state.db.Set([]byte(user2.PublicKey), userJSON2)
	return user1, 1
}
