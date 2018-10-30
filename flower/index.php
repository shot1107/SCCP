<?php // 振り分けプログラム
$src = empty($_GET['src']) ? 'sakura' : $_GET['src'];
// ディレクトリを確認
$dir_src = dirname(__FILE__)."/$src";
if (!file_exists($dir_src)) die("振り分け対象がありません");
$dir_ok = $dir_src.'-ok';
$dir_ng = $dir_src.'-ng';
if (!file_exists($dir_ok)) { // ディレクトリの作成
  mkdir($dir_ok);
  mkdir($dir_ng);
}
// 何をするかURL引数に応じて処理を変える
$m = empty($_GET['m']) ? 'show' : $_GET['m'];
if ($m == 'show') { // 画像を表示する
  $files = glob("./{$src}/*.jpg");
  if (!$files) die("もう画像がありません。");
  $file = $files[0];
  echo '<meta name="viewport" content="width=320">';
  echo "<img src='$file' width='300'><br>";
  $f = basename($file);
  echo "<a href='index.php?src=$src&m=ok&f=$f'>[OK]</a> ---";
  echo "<a href='index.php?src=$src&m=ng&f=$f'>[NG]</a>";
} else if ($m == 'ok' || $m == 'ng') { // 移動を行う
  $f = empty($_GET['f']) ? '' : $_GET['f'];
  $file = "$dir_src/$f";
  $moveto = "{$dir_src}-{$m}/$f";
  if (!file_exists($file)) die("ファイルがありません");
  $b = @rename($file, $moveto);
  if (!$b) die("ファイルの移動に失敗しました");
  header("location: ./index.php?src=$src");
}
