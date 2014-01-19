package com.postpushr;

import java.io.ByteArrayInputStream;
import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.Security;

import org.apache.http.util.ByteArrayBuffer;
import org.spongycastle.crypto.digests.SHA1Digest;
import org.spongycastle.jce.provider.BouncyCastleProvider;
import org.spongycastle.util.encoders.Hex;

import android.app.Activity;
import android.os.Bundle;

import com.postpushr.SignInFragment.SignInListener;


public class SignInActivity extends Activity implements SignInListener {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_signin);		
		getFragmentManager().beginTransaction().add(R.id.signin_fragment_container, new SignInFragment()).commit();
	}

	@Override
	public void onLoginButton() {
		getFragmentManager().beginTransaction().replace(R.id.signin_fragment_container, new LoginFragment()).addToBackStack("Replace with LoginFragment").commit();
	}

	@Override
	public void onRegisterButton() {
		getFragmentManager().beginTransaction().replace(R.id.signin_fragment_container, new RegisterFragment()).addToBackStack("Replace with RegisterFragment").commit();
	}

	private String hashPassword(String password) {
		return Util.Sha1Hash(Util.Sha1Hash(password) + Util.Sha1Hash(Secrets.getSalt()));
	}


	/*@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.setup_actions, menu);
		return super.onCreateOptionsMenu(menu);
	}*/

}
