package com.example.androidgg;

import android.os.Bundle;
import android.os.Handler;
import android.app.Activity;
import android.view.Menu;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
	WebView wv_contenido;
	private Handler handler = new Handler();
	private Runnable runnable = new Runnable() {
		   @Override
		   public void run() {
			  //wv_contenido.loadUrl("http://192.168.1.1/");


			   wv_contenido.loadUrl("http://192.168.43.5:9090/androi");
			   
			  //http://onlineclock.net/
		      handler.postDelayed(this, 5000);
		   }
		};
	//
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		wv_contenido=(WebView)this.findViewById(R.id.wv_contenido);
		   wv_contenido.setWebViewClient(new WebViewClient() {
		        @Override
		        public void onReceivedError(WebView view, int errorCode,
		                String description, String failingUrl) {
		            // Handle the error
		        }

		        @Override
		        public boolean shouldOverrideUrlLoading(WebView view, String url) {
		            view.loadUrl(url);
		            return true;
		        }
		    });
		handler.postDelayed(runnable, 100);
		//wv_contenido.loadUrl("http://192.168.1.1/");
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
