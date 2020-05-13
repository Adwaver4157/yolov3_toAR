import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

//サイズが大きいのでImages, Annotationは削除してある
//再現するときは, http://vision.stanford.edu/aditya86/ImageNetDogs/からdownloadして直下に移動
public class A {
    public static final long mod = (long)1e9+7;
    public static final long INF = Long.MAX_VALUE/2;
    public static final int inf = Integer.MAX_VALUE/2;

    static void solve(InputReader in, PrintWriter out){
        File outer_file = new File("Annotation");
        String[] folders = outer_file.list();

        FileReader fr;
        FileWriter fw, class_fw;
        BufferedReader br;
        int img_number = 0;  // imgの番号
        int class_number = 0;  // クラスの番号
        try{
            class_fw = new FileWriter("datasets/img"+img_number+".txt");
            for (String s: folders) {
                if(s.length()<10) continue;  // いらないのが一つある
                String fIle_name = "Annotation/"+s+"/";
                File inner_file = new File(fIle_name);
                String[] files = inner_file.list();
                for(String t: files){
                    fr = new FileReader(fIle_name+t); // 拡張子なし！
                    br = new BufferedReader(fr);
                    for (int i = 0; i < 18; i++) br.readLine();

                    char[] line = new char[0];
                    //数字を読み取る
                    int[] xy = new int[4];  // xmin,ymin,xmax,ymaxの順
                    for (int i = 0; i < 4; i++) {
                        line = br.readLine().toCharArray();
                        int a = 0;
                        for (char c : line) {
                            if (c <= '9' && c >= '0') {
                                a *= 10;
                                a += (c - '0');
                            }
                        }
                        xy[i] = a;
                    }

                    //複数の犬がいるのは使わない
                    for (int i = 0; i < 3; i++) line = br.readLine().toCharArray();
                    if(line[0]!='<') continue;

                    //xyからtxtを作成
                    /*
                    fw = new FileWriter("datasets/img"+img_number+".txt");
                    fw.write(Integer.toString(class_number));
                    fw.write(' ');
                    fw.write(Integer.toString((xy[2]+xy[0])/2));
                    fw.write(' ');
                    fw.write(Integer.toString((xy[3]+xy[1])/2));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[2]-xy[0]));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[3]-xy[1]));
                    fw.write("\n");
                    fw.close();
                    */
                    // keras版はclass,xmin,ymin,xmax,ymaxらしい
                    fw = new FileWriter("datasets/img"+img_number+".txt");
                    fw.write(Integer.toString(class_number));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[0]));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[1]));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[2]));
                    fw.write(' ');
                    fw.write(Integer.toString(xy[3]));
                    fw.write("\n");
                    fw.close();

                    //画像の移動
                    Path sourcePath = Paths.get("Images/"+s+"/"+t+".jpg");
                    Path targetPath = Paths.get("datasets/img"+img_number+".jpg");
                    Files.copy(sourcePath, targetPath);

                    img_number++;
                }
                class_number++;
            }
        }catch (Exception e){
            //何もしない
        }

    }

    public static void main(String[] args){
        InputReader in = new InputReader(System.in);
        PrintWriter out = new PrintWriter(System.out);
        solve(in, out);
        out.close();
    }
    public static class InputReader{
        private BufferedReader br;
        private StringTokenizer st;
        public InputReader(InputStream is){
            br = new BufferedReader(new InputStreamReader(is));
            st = null;
        }
        public String ns(){
            if(st == null || !st.hasMoreTokens()){
                try{
                    st = new StringTokenizer(br.readLine());
                }catch (Exception e){
                    throw new RuntimeException(e);
                }
            }
            return st.nextToken();
        }
        public int ni(){
            return Integer.parseInt(ns());
        }
        public long nl(){
            return Long.parseLong(ns());
        }
        public double nd(){
            return Double.parseDouble(ns());
        }
        public char nc(){
            return ns().toCharArray()[0];
        }
        public int[] ni(int n){
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = ni();
            }
            return a;
        }
        public long[] nl(int n){
            long[] a = new long[n];
            for (int i = 0; i < n; i++) {
                a[i] = nl();
            }
            return a;
        }
        public double[] nd(int n){
            double[] a = new double[n];
            for (int i = 0; i < n; i++) {
                a[i] = nd();
            }
            return a;
        }
    }
}